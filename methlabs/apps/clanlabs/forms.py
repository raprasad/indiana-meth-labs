from django.forms import ModelForm

from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod, ClandestineLabReport


class ClandestineLabReportForm(ModelForm):
     class Meta:
         model = ClandestineLabReport
         exclude = ('created', 'modified')
