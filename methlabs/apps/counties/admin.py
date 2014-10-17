from django.contrib import admin
from apps.counties.models import County

admin.site.register(County)

class CountyAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'slug', )
    search_fields = ('name',)
    readonly_fields = ('modified', 'created', )

# admin.site.register(County, CountyAdmin)

