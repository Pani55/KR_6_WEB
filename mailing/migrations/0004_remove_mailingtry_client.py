# Generated by Django 4.2.2 on 2024-08-10 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0003_alter_mailing_next_send_datetime"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mailingtry",
            name="client",
        ),
    ]
