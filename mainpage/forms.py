from django import forms
from .models import Reservation
from django.utils import timezone
from django.contrib import messages

class ReservationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Reservation
        fields = ['datetime']
        widgets = {
            'datetime': forms.DateTimeInput(attrs = {'type': 'datetime-local'}, format = '%d-%m-%YT%H:%M'),
        }

    def clean(self):
        cleaned_data = super().clean()
        datetime_value = cleaned_data.get('datetime')

        if datetime_value:
            current_datetime = timezone.localtime(timezone.now())
            rounded_current_time = current_datetime.replace(minute = 0, second = 0, microsecond = 0)

            if datetime_value < current_datetime:
                messages.error(self.request, 'Reservation date cannot be in the past.')
                raise forms.ValidationError('Reservation date cannot be in the past.')
            elif datetime_value <= rounded_current_time:
                messages.error(self.request, 'Reservation time must be at least one hour in the future and rounded to the next full hour.')
                raise forms.ValidationError('Reservation time must be at least one hour in the future and rounded to the next full hour.')
            elif not (8 <= datetime_value.hour <= 23):
                messages.error(self.request, 'Reservation hour must be between 8am and 11pm.')
                raise forms.ValidationError('Reservation hour must be between 8am and 11pm.')
            elif datetime_value.minute != 0:
                messages.error(self.request, 'Reservation must be made for a round hour.')
                raise forms.ValidationError('Reservation must be made for a round hour.')

        return cleaned_data
