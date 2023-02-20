import logging
from datetime import timedelta

import requests
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


@shared_task(name='send_push_order_confirmed')
def send_push_order_confirmed_task(order_id: int) -> None:
    """Таска для отправки пуш уведомления подтверждения записи"""

    from apps.profile.models import Profile
    from apps.salon.models import Order

    order = Order.objects.filter(id=order_id).first()

    if order and order.user and order.status == 'confirmed':
        profile = Profile.objects.filter(expo_token__isnull=False, user=order.user).first()

        date = (order.date + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')
        title = 'Подтверждение записи'
        text = f'Вы записаны в салон {order.salon.name}\n{date} (Мск).\n' \
               f'Подробнее в личном кабинете'

        if profile:
            try:
                send_push_notification(
                    profile.expo_token, title, text
                )
            except DeviceNotRegisteredError:
                profile.expo_token = None
                profile.save(update_fields='expo_token')


@shared_task(name='send_to_telegram')
def send_salon_new_order_to_telegram_task(order_id):
    """Таска отправки сообщения в телеграмм"""

    from apps.salon.models import Order
    from apps.salon.models import TgSettings

    order = Order.objects.filter(id=order_id).first()
    salon_name = order.salon.name if order.salon else "-"
    name = order.name if order.name else "-"
    service_name = order.service.name if order.service else "-"
    spec_name = order.spec.name if order.spec else "-"
    date = (order.date + timedelta(hours=3)).strftime('%Y-%m-%d %H:%M')

    message = f'Поступление новой заявки\n' \
              f'Источник: {order.source}\n' \
              f'Салон: {salon_name}\n' \
              f'Телефон: {order.phone}\n' \
              f'Имя: {name}\n' \
              f'Услуга: {service_name}\n' \
              f'Специалист: {spec_name}\n' \
              f'Дата: {date} (Мск)'

    if order and order.salon and order.status == 'new':
        bot = TgSettings.objects.filter(salon_id=order.salon_id, is_publish=True).first()
        if bot and bot.token and bot.chats:
            url = f'https://api.telegram.org/bot{bot.token}/sendMessage'
            for chat in bot.chats.all():
                try:
                    requests.post(url, {'chat_id': chat.chat_id, 'text': message})
                except Exception as e:
                    logger.exception('Send telegram exception\n', str(e))
