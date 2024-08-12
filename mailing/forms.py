from django.forms import ModelForm, BooleanField
from django import forms
from mailing.models import Mailing, Message, Client


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].queryset = Message.objects.filter(owner=self.instance.owner)
        self.fields['clients'].queryset = Client.objects.filter(owner=self.instance.owner)

    class Meta:
        model = Mailing
        fields = ['name',
                  'last_send_datetime', 'period', 'message',
                  'clients']
        widgets = {
            'last_send_datetime': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}),
            # multiple select for many-to-many relation
            'clients': forms.SelectMultiple(
                attrs={'multiple': True}),
        }


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = ['mail_theme', 'message']


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
