from tastypie.resources import ModelResource

from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod, ClandestineLabReport



class SeizureLocationTypeResource(ModelResource):
    class Meta:
        queryset = SeizureLocationType.objects.all()
        resource_name = 'seizure-location-type'
        
class ManufacturingMethodResource(ModelResource):
    class Meta:
        queryset = ManufacturingMethod.objects.all()
        resource_name = 'manufacturing-method'
    
class ClanLabReportResource(ModelResource):
    class Meta:
        queryset = ClandestineLabReport.objects.all()
        resource_name = 'clandestine-lab-report'
        excludes = ['is_visible', 'created', 'modified']