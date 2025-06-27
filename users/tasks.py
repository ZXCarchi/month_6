from celery import shared_task
import time
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import random
from django.core.cache import cache

@shared_task
def send_otp_email(user_email, code):
    print("Sending ...")
    time.sleep(20)
    print("Email sent")


@shared_task
def send_daily_report():
    print("Sending daily report...")
    time.sleep(40)
    print("Daily report sent")


@shared_task
def send_otp(email):
    code = str(random.randint(100000, 999999))
    cache.set(f"otp:{email}", code, timeout=300)
    send_mail(
        subject='Ваш код подтверждения',
        message=f'Ваш OTP: {code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )


@shared_task
def send_hourly_greetings():
    from django.contrib.auth import get_user_model
    from django.utils import timezone

    User = get_user_model()
    now = timezone.now()
    for u in User.objects.filter(is_active=True):
        send_mail(
            subject='Привет!',
            message=f'Привет, {u.username}! Сейчас {now.strftime("%H:%M")}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[u.email],
            fail_silently=True,
        )