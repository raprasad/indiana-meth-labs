from django.db import models
from model_utils.models import TimeStampedModel
from hashlib import md5
from datetime import datetime

class SharedReportRecord(TimeStampedModel):
    """
    Information from API call: https://api.github.com/repos/iqss/dataverse/milestones
    """
 
    report_month = models.DateField()
    to_email = models.EmailField()
    from_name =  models.CharField(max_length=100)
    from_email = models.EmailField()
    full_message = models.TextField(blank=True)
    
    md5 = models.CharField(max_length=40, blank=True, db_index=True, help_text='auto-filled on save')
    
    
    def __unicode__(self):
        return 'Report Month %s' % (self.report_month)
    
    def save(self, *args, **kwargs):
         if not self.id:
             super(SharedReportRecord, self).save(*args, **kwargs)

         self.md5 = md5('%s%s%s' % (str(datetime.now()), self.id, self.report_month)).hexdigest()

         super(SharedReportRecord, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created', )