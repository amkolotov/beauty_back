import logging

from celery import shared_task
from exponent_server_sdk import PushClient, PushMessage, PushServerError,\
    DeviceNotRegisteredError, PushTicketError
from requests.exceptions import ConnectionError, HTTPError

logger = logging.getLogger('tasks')


def send_push_notification(token: str, title: str, message: str, extra: dict = None) -> None:
    """Отправляет пуш уведомления"""

    try:
        response = PushClient().publish(
            PushMessage(to=token,
                        title=title,
                        body=message,
                        data=extra))

    except PushServerError as exc:
        # Encountered some likely formatting/validation error.
        data = {
                'token': token,
                'title': title,
                'message': message,
                'extra': extra,
                'errors': exc.errors,
                'response_data': exc.response_data,
            }
        logger.exception('PushServerError: %s', data)
        raise

    except (ConnectionError, HTTPError) as exc:
        # Encountered some Connection or HTTP error - retry a few times in
        # case it is transient.
        data = {'token': token, 'title': title, 'message': message, 'extra': extra}
        logger.exception('ConnectionError, HTTPError: %s', data)
        raise

    try:
        # We got a response back, but we don't know whether it's an error yet.
        # This call raises errors so we can handle them with normal exception
        # flows.
        response.validate_response()

    except DeviceNotRegisteredError:
        logger.exception('DeviceNotRegisteredError: %s', token)
        # Mark the push token as inactive
        raise

    except PushTicketError as exc:
        # Encountered some other per-notification error.
        data = {
                'token': token,
                'title': title,
                'message': message,
                'extra': extra,
                'push_response': exc.push_response._asdict(),
            }
        logger.exception('PushTicketError: %s', data)
        raise


@shared_task(name='send_push_notifications')
def send_push_notifications_task(notification_id: int) -> None:
    """Таска для отправки пуш уведомления"""

    from apps.profile.models import Profile
    from apps.salon.models import Notification

    notification = Notification.objects.filter(id=notification_id).first()

    if notification and notification.is_publish:
        profiles_qs = Profile.objects.filter(expo_token__isnull=False)

        if notification.for_users.exists():
            profiles_qs = profiles_qs.filter(user__in=notification.for_users.all())
        elif notification.for_salons.exists():
            profiles_qs = profiles_qs.filter(salon__in=notification.for_salons.all())

        for profile in profiles_qs:
            try:
                send_push_notification(
                    profile.expo_token, notification.title, notification.text
                )
            except DeviceNotRegisteredError:
                profile.expo_token = None
                profile.save(update_fields='expo_token')
