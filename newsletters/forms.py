from django import forms

from newsletters.models import Recipient, Message, Distribution


class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ['email', 'name', 'comment']

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите email'
        })

        self.fields['name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите ФИО'
        })

        self.fields['comment'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите комментарий'
        })


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['theme', 'text_letter']

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)

        self.fields['theme'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите тему'
        })

        self.fields['text_letter'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите текст письма'
        })


class DistributionForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = ['status', 'message', 'recipient']

    def __init__(self, *args, **kwargs):
        super(RecipientForm, self).__init__(*args, **kwargs)

        self.fields['status'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите статус рассылки'
        })

        self.fields['message'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите письмо для рассылки'
        })

        self.fields['recipient'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите получателей рассылки'
        })
