from django import forms

from wellcome.models import Subscriber


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        exclude = ['']