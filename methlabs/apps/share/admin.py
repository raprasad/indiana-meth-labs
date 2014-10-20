from django.contrib import admin

from apps.share.models import SharedReportRecord


class SharedReportRecordAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('from_name', 'from_email','to_email', 'report_month', 'created',   )
    readonly_fields = ('modified', 'created', 'md5' )
admin.site.register(SharedReportRecord, SharedReportRecordAdmin)
