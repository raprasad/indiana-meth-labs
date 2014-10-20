from django.db import models
from django.utils.text import slugify

from model_utils.models import TimeStampedModel
from apps.counties.models import County, Town
from apps.clanlabs.validators import validate_report_date

class SeizureLocationType(TimeStampedModel):

    name = models.CharField(max_length=100, unique=True)    
    sort_order = models.IntegerField(default=10)
    slug = models.SlugField(blank=True, help_text='auto-filled on save')
    
    def __unicode__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SeizureLocationType, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ('sort_order', 'name', )
        

class ManufacturingMethod(TimeStampedModel):
    
    name = models.CharField(max_length=100, unique=True)    
    description = models.TextField(blank=True)
    sort_order = models.IntegerField(default=10)
    slug = models.SlugField(blank=True, help_text='auto-filled on save')
    
    def __unicode__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ManufacturingMethod, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ('sort_order', 'name', )
        


CASE_NUMBER_NOT_AVAILABLE = 'Not Available'
NON_INDIANA_STATE_POLICE = 'NON-ISP'
class ClandestineLabReport(TimeStampedModel):
    
    case_number = models.CharField(max_length=255, db_index=True)
    
    report_date = models.DateField(db_index=True, validators=[validate_report_date])

    is_visible = models.BooleanField(default=True, db_index=True)

    town = models.ForeignKey(Town)
    county = models.ForeignKey(County, null=True, blank=True)
    
    address = models.CharField(max_length=255)
    
    lng_position = models.DecimalField (max_digits=17, decimal_places=15, blank=True, null=True)
    lat_position = models.DecimalField (max_digits=17, decimal_places=15, blank=True, null=True)
    
    manufacturing_methods = models.ManyToManyField(ManufacturingMethod, blank=True, null=True)
    seizure_location_types = models.ManyToManyField(SeizureLocationType, blank=True, null=True)
    
    # lab number
    lab_number = models.CharField(max_length=255, db_index=True)    
    non_isp_lab = models.BooleanField('Local police', default=False, help_text='Not Indiana State Police.  Contact local law enforcement for more information.')
    
    # optional
    vin_number = models.CharField('Vehicle ID#', max_length=255, blank=True)
    pdf_report_link = models.URLField(blank=True)
    
    def __unicode__(self):
        return '%s (%s)' % (self.lab_number, self.id)

    def display_locations(self):
        return '\n'.join(self.seizure_location_types.values_list('name', flat=True).all())
    display_locations.allow_tags = True

    def save(self, *args, **kwargs):

        self.slug = slugify('%s %s' % (self.address, self.town))

        self.county = self.town.county

        if self.lab_number == NON_INDIANA_STATE_POLICE:
            self.non_isp_lab = True
        else:
            self.non_isp_lab = False
        super(ClandestineLabReport, self).save(*args, **kwargs)

    class Meta:
        ordering = ('report_date', )
    

# For presentation, to show 1 line admin
#
class SeizureLocationTypeProxy(SeizureLocationType):
    class Meta:
        verbose_name = 'Seizure location type (simple admin)'
        verbose_name_plural = 'Seizure location types (simple admin)'
        proxy = True
    