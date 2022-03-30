from django import forms


class TimePickerInput(forms.TimeInput):
    input_type = 'time'


class DatePickerInput(forms.DateInput):
    input_type = 'date'


class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime'
