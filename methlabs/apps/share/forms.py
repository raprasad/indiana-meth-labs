from django import forms

from apps.share.models import SharedReportRecord

class SharedReportRecordForm(forms.ModelForm):
    class Meta:
        model = SharedReportRecord
        widgets = {'report_month': forms.HiddenInput() }
        
        exclude = ['full_message', 'md5', 'created', 'modified']

    def clean(self):
        
        personal_note
        