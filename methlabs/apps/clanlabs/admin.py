from django.contrib import admin

from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod, SeizureLocationTypeProxy, ClandestineLabReport

class SeizureLocationTypeAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'sort_order', 'slug' )
    search_fields = ('name',)
    list_editable = ('sort_order',)
    readonly_fields = ('modified', 'created' )
admin.site.register(SeizureLocationType, SeizureLocationTypeAdmin)


admin.site.register(SeizureLocationTypeProxy)

class ManufacturingMethodAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'slug', 'sort_order', 'description')
    search_fields = ('name', 'description')
    list_editable = ('sort_order',)
    readonly_fields = ('modified', 'created' )
admin.site.register(ManufacturingMethod, ManufacturingMethodAdmin)


class ClandestineLabReportAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('report_date', 'case_number','lab_number', 'is_visible', 'non_isp_lab', 'county', 'address')
    search_fields = ('case_number', 'lab_number','address', 'manufacturing_methods__name' )
    list_filter = ('is_visible', 'non_isp_lab', 'manufacturing_methods', 'seizure_location_types', 'county' )
    
    readonly_fields =  ('modified', 'created', 'non_isp_lab', 'county', 'display_locations')
    
    filter_horizontal = ('manufacturing_methods', 'seizure_location_types',)
    
    fieldsets = (
         ('Case / Date / Location', {
                  'fields': (('case_number', 'report_date',  )\
                  , 'pdf_report_link'
                  )
          }),    
          ('Lab Info', {
                   'fields': ('lab_number'\
                   , 'non_isp_lab'\
                   , 'manufacturing_methods'\
                   )
           }),
           ('Location Info', {
                    'fields': ( 'county', 'town'\
                    , 'address'\
                    , ('lat_position', 'lng_position',)\
                    , 'seizure_location_types'\
                    )
            }),
           ('Vehicle Information', {
                  'fields': ('vin_number', )
           }),
           ('Read-Only Info', {
               'fields': (('modified', 'created') )
           }),
       )
admin.site.register(ClandestineLabReport, ClandestineLabReportAdmin)

