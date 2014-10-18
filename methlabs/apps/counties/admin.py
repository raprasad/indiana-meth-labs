from django.contrib import admin
from apps.counties.models import County, Town

#admin.site.register(County)

class CountyAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'slug', )
    search_fields = ('name',)
    readonly_fields = ('modified', 'created', )
admin.site.register(County, CountyAdmin)



class TownAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'county', 'county_name', 'slug')
    search_fields = ('name', 'county_name')
    readonly_fields = ('modified', 'created', )
admin.site.register(Town, TownAdmin)
