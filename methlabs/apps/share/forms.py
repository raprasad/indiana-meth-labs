from django import forms

from apps.share.models import SharedReportRecord

class SharedReportRecordForm(forms.ModelForm):
    class Meta:
        model = SharedReportRecord
        widgets = {'report_month': forms.HiddenInput() }
        exclude = ['full_message', 'md5', 'created', 'modified']

    def clean(self):
        
        from_email = self.cleaned_data.get('from_email')
        to_email = self.cleaned_data.get('to_email')
           
        if from_email and to_email:
            if from_email == to_email:
                msg = 'Why are you sending email to yourself'
                self._errors["to_email"] = self.error_class([msg])

                self._errors["from_email"] = self.error_class([msg2])
                msg2 = 'To and From email cannot be the same'
            
        return self.cleaned_data