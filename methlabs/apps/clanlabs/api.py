from tastypie.resources import ModelResource

from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod, ClandestineLabReport


class SeizureLocationTypeResource(ModelResource):
    class Meta:
        queryset = SeizureLocationType.objects.all()
        resource_name = 'seizure-location-type'
        excludes = [ 'created', 'modified']
        
class ManufacturingMethodResource(ModelResource):
    class Meta:
        queryset = ManufacturingMethod.objects.all()
        resource_name = 'manufacturing-method'
        excludes = [ 'created', 'modified']
        
class ClanLabReportResource(ModelResource):
    
    
    def dehydrate(self, bundle):
        r = bundle.obj
        
        bundle.data['town'] = r.town
        bundle.data['county'] = r.county
        bundle.data['manufacturing_methods'] = [ x.name for x in r.manufacturing_methods.all()]
        bundle.data['seizure_location_types'] = [ x.name for x in r.seizure_location_types.all()]
        
        return bundle
        
    class Meta:
        queryset = ClandestineLabReport.objects.all()
        resource_name = 'clandestine-lab-report'
        excludes = ['is_visible', 'created', 'modified']