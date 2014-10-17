from django.db import models

from django.utils.text import slugify

class County(models.Model):

    name = models.CharField(max_length=100, unique=True)
    
    geojson = models.TextField(blank=True)
    slug = models.SlugField(blank=True, help_text='auto-filled on save')

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    
    def __unicode__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(County, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = 'Counties'
        ordering = ('name', )
    