# Generated by Django 4.2.2 on 2024-08-10 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="first_send_datetime",
            field=models.DateTimeField(
                auto_now_add=True, verbose_name="дата первого отправления"
            ),
        ),
    ]
