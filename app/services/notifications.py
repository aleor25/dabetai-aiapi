from pyfcm import FCMNotification
from app.core.config import settings

_FCM = None


def get_fcm():
    global _FCM
    if _FCM is None:
        _FCM = FCMNotification(api_key=settings.fcm_server_key)
    return _FCM


def send_notification(token: str, title: str, body: str, data_message: dict = None):
    push_service = get_fcm()
    result = push_service.notify_single_device(registration_id=token, message_title=title, message_body=body, data_message=data_message)
    return result
