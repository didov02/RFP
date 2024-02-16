from django import forms
from .models import Reservation
from django.utils import timezone

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['datetime']
        widgets = {
            'datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%d-%m-%YT%H:%M'),
        }

    def clean(self):
        cleaned_data = super().clean()
        datetime_value = cleaned_data.get('datetime')

        if datetime_value:
            current_datetime = timezone.localtime(timezone.now())

            if datetime_value < current_datetime:
                raise forms.ValidationError('Reservation datetime cannot be in the past.')

            rounded_current_time = current_datetime.replace(minute=0, second=0, microsecond=0)

            if datetime_value <= rounded_current_time:
                raise forms.ValidationError('Reservation datetime must be at least one hour in the future and rounded to the next full hour.')

            if not (8 <= datetime_value.hour <= 23):
                raise forms.ValidationError('Reservation hour must be between 8am and 11pm.')
            
            if datetime_value.minute != 0:
                raise forms.ValidationError('Reservation must be made for a round hour.')

        return cleaned_data
