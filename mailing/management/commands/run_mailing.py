# run_mailing.py
import smtplib
from datetime import datetime
import pytz
from django.core.mail import send_mail
from django.core.management.base import BaseCommand

from config import settings
from mailing.models import Mailing, MailingTry

zone = pytz.timezone(settings.TIME_ZONE)


class Command(BaseCommand):

    def handle(self, *args, **options):
        mailings = Mailing.objects.filter(status__in=[0, 1])

        if mailings:
            for mailing in mailings:
                clients = mailing.clients.all()
                try:
                    send_mail(
                        subject=mailing.message.mail_theme,
                        message=mailing.message.message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email for client in clients],
                        fail_silently=False,
                    )
                    MailingTry.objects.create(
                        mailing=mailing,
                        status=True,
                        response='',
                        try_datetime=datetime.now(zone)
                    )
                except smtplib.SMTPException as e:
                    MailingTry.objects.create(
                        mailing=mailing,
                        status=False,
                        response=str(e),
                        try_datetime=datetime.now(zone)
                    )
        else:
            print("Нет активных рассылок")
