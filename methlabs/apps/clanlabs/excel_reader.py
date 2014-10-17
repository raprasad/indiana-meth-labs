import xlrd
from os.path import isfile

from django.conf import settings
from apps.counties.models import County


COLUMN_HEADERS = ('report_date', 'county', 'location', 'vin_number', 'pdf_report', 'clean_cert', 'case_number', 'lab_number', 'residence', 'outbuilding', 'vehicle', 'hotel_motel', 'open', 'business', 'other', 'red_p', 'nazi', 'onepot') 

BOOLEAN_COLUMN_HEADERS = COLUMN_HEADERS[-10:]

class RowFormatter:

    def __init__(self, row):
        assert len(row) == len(COLUMN_HEADERS)
        for idx, col_val in enumerate(row):
            self.__dict__[COLUMN_HEADERS[idx]] = col_val
    
        
class ExcelReader:
    
    def __init__(self, fname):
        assert isfile(fname) is True, "Not a file: %s" % fname
        
        self.fname = fname
        