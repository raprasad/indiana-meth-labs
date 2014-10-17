from django.db import models
from django.utils.text import slugify

from model_utils.models import TimeStampedModel
from apps.counties.models import County
from apps.clanlabs.validators import validate_report_date

class SeizureLocationType(TimeStampedModel):

    name = models.CharField(max_length=100, unique=True)    
    sort_order = models.IntegerField(default=10)
    slug = models.SlugField(blank=True, help_text='auto-filled on save')
    
    def __unicode__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SeizureLocation, self).save(*args, **kwargs)
        
    class Meta:
        ordering = ('sort_order', 'name', )
        
        
MANUFACTURING_METHOD_NOT_SPECIFIED = 'Not Specified'
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
        
        
class ClandestineLabReport(TimeStampedModel):
    
    case_number = models.CharField(max_length=255, unique=True)
    
    report_date = models.DateField(validators=[validate_report_date])
        
    county = models.ForeignKey(County)
    address = models.CharField(max_length=255)
    
    lng_position = models.DecimalField (max_digits=8, decimal_places=3)
    lat_position = models.DecimalField (max_digits=8, decimal_places=3)
    
    manufacture_method = models.ForeignKey(ManufacturingMethod)
    seizure_location_type = models.ManyToManyField(SeizureLocationType, blank=True, null=True)
    
    # lab number
    lab_number = models.CharField(max_length=255, blank=True)    
    non_isp_lab = models.BooleanField('non-Indiana State Police', default=False, help_text='Contact local law enforcement for more information. (auto-filled on save)')
    
    # optional
    vin_number = models.CharField('Vehicle ID#', max_length=255, blank=True)
    pdf_report_link = models.URLField(blank=True)
    
    def __unicode__(self):
           return '%s (%s)' % (self.name, self.id)

    def save(self, *args, **kwargs):
       self.slug = slugify(self.name)
       super(ClandestineLabReport, self).save(*args, **kwargs)

       class Meta:
           ordering = ('name', )
    
    