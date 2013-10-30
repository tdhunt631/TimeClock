from django.forms import ModelForm
from django import forms

from clock.models import Record

class AddRecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['project']

class UpdateRecordForm(ModelForm):
    class Meta:
        model = Record
        fields = ['project', 'startTime', 'endTime', 'note']

class AddNoteForm(ModelForm):
	class Meta:
		model = Record
		fields = ['note']

class DateRangeForm(forms.Form):
    from_date = forms.DateField()
    to_date = forms.DateField()
