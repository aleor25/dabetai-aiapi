from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user
from app.schemas.patient import PatientCreate, PatientOut, PatientUpdate
from app.crud import crud_patient
from typing import Optional

router = APIRouter()


@router.get('/', response_model=dict)
def list_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None, description="Search by patient name or CURP"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    List patients with pagination and search.
    - skip: offset for pagination
    - limit: max results per page
    - search: search by name or CURP
    """
    items, total = crud_patient.list_patients(db, current_user.id, skip=skip, limit=limit, q=search)
    # Ensure all items are properly converted to dicts for JSON serialization
    serialized_items = [PatientOut.model_validate(item).model_dump() for item in items]
    return {
        "items": serialized_items,
        "total": total,
        "skip": skip,
        "limit": limit
    }


@router.post('/', response_model=PatientOut, status_code=201)
def create_patient(patient_in: PatientCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Create a new patient for the current doctor."""
    p = crud_patient.create_patient(db, current_user.id, patient_in)
    return p


@router.get('/{patient_id}', response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Get patient details (only accessible by their doctor)."""
    p = crud_patient.get_patient(db, patient_id)
    if not p or p.doctor_id != current_user.id:
        raise HTTPException(status_code=404, detail='Patient not found')
    return p


@router.put('/{patient_id}', response_model=PatientOut)
def update_patient(
    patient_id: int,
    patient_update: PatientUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Update patient information (only by their doctor)."""
    p = crud_patient.get_patient(db, patient_id)
    if not p or p.doctor_id != current_user.id:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    # Update fields that were provided
    update_data = patient_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(p, field, value)
    
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.delete('/{patient_id}', status_code=204)
def delete_patient(patient_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Delete a patient (soft or hard delete)."""
    p = crud_patient.get_patient(db, patient_id)
    if not p or p.doctor_id != current_user.id:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    db.delete(p)
    db.commit()
    return None
