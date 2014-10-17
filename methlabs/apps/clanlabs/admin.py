from django.contrib import admin

from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod, ClandestineLabReport

class SeizureLocationTypeAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'sort_order', 'slug' )
    search_fields = ('name',)
    list_editable = ('sort_order',)
    readonly_fields = ('modified', 'created' )
admin.site.register(SeizureLocationType, SeizureLocationTypeAdmin)


class ManufacturingMethodAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('name', 'slug', 'sort_order', 'description')
    search_fields = ('name', 'description')
    list_editable = ('sort_order',)
    readonly_fields = ('modified', 'created' )
admin.site.register(ManufacturingMethod, ManufacturingMethodAdmin)


class ClandestineLabReportAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('case_number', 'report_date', 'county')
    search_fields = ('case_number', 'address', 'manufacture_method__name' )
    list_filter = ('county', 'manufacture_method', 'seizure_location_type' )
    readonly_fields =  ('modified', 'created', 'non_isp_lab')
    filter_horizontal = ('seizure_location_type',)
    fieldsets = (
         ('Case / Date / Location', {
                  'fields': (('case_number', 'report_date',  )\
                  , 'pdf_report_link'
                  )
          }),    
          ('Lab Info', {
                   'fields': (('lab_number', 'non_isp_lab',  )\
                   , 'manufacture_method'\
                   )
           }),
           ('Location Info', {
                    'fields': ( ('county', 'address')\
                    , ('lat_position', 'lng_position',)\
                    , 'seizure_location_type'\
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

