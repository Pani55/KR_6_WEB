from django.contrib import admin

from mailing.models import Mailing, Message, Client, MailingTry


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('name', 'period', 'status', 'owner')
    list_filter = ('status', 'owner')
    search_fields = ('name',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('mail_theme', 'message', 'owner')
    list_filter = ('owner', 'mail_theme')
    search_fields = ('mail_theme',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'comment', 'owner')
    list_filter = ('owner',)
    search_fields = ('owner',)


@admin.register(MailingTry)
class MailingTryAdmin(admin.ModelAdmin):
    list_display = ('try_datetime', 'status', 'response')
    list_filter = ('try_datetime', 'status')
