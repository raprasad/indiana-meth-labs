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
from django.conf import settings
print 'EMAIL_HOST', settings.EMAIL_HOST
print 'EMAIL_HOST_USER', settings.EMAIL_HOST_USER
print 'EMAIL_HOST_PASSWORD', settings.EMAIL_HOST_PASSWORD
print 'EMAIL_PORT', settings.EMAIL_PORT
print 'EMAIL_USE_TLS', settings.EMAIL_USE_TLS
print 'DEFAULT_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL
print 'SERVER_EMAIL', settings.SERVER_EMAIL 

from django.core.mail import send_mail
send_mail('Test django email #4', 'Test meth lab list from django app.', 'raprasad@gmail.com',\
    ['raman_prasad@harvard.edu', 'raprasad@gmail.com'], fail_silently=False)
"""