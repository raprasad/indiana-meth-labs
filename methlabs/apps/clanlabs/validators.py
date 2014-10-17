from datetime import datetime, date
from django.core.exceptions import ValidationError


FIRST_REPORT_YEAR = 2007
def validate_report_date(report_date):
    if not type(report_date) is date:
        raise ValidationError(u'The date cannot be type: %s' % type(report_date))
    
    today = date.today()
    if report_date > today:
        raise ValidationError(u'The report date cannot be in the future.  Today is: %s' % today)

    if report_date.year < FIRST_REPORT_YEAR:
        raise ValidationError(u'The report date cannot before the year: %s' % FIRST_REPORT_YEAR)



"""
send_mail('Test django email', 'Test meth lab list from django app.', 'raman_prasad@harvard.edu',\
    ['raman_prasad@harvard.edu'], fail_silently=False)
"""