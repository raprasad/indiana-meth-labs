from __future__ import print_function
from django import forms

from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod, ClandestineLabReport

class MethImportForm(forms.Form):
    """Used to read CSV file with Meth Data"""
    
    report_date = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M:%S AM', '%m/%d/%Y %H:%M:%S PM'])
    county = forms.CharField(max_length=100)
    location = forms.CharField(label='address, lat, lng', max_length=255)

    vin_number = forms.CharField(max_length=100, required=False)
    pdf_report = forms.URLField(max_length=255, required=False)
    clean_cert = forms.CharField(max_length=100, required=False)
    
    case_number = forms.CharField(max_length=70, required=False)
    lab_number = forms.CharField(max_length=255, required=False)

    # seizure location
    residence = forms.BooleanField(required=False)
    outbuilding = forms.BooleanField(required=False)
    vehicle = forms.BooleanField(required=False)
    hotel_motel = forms.BooleanField(required=False)
    open_area = forms.BooleanField(required=False)
    business = forms.BooleanField(required=False)
    other = forms.BooleanField(required=False)

    # manufacture types
    red_p = forms.BooleanField(required=False)
    nazi = forms.BooleanField(required=False)
    onepot = forms.BooleanField(required=False)

    def clean_report_date(self):
        rd = self.cleaned_data.get('report_date', None)
        if rd is None:
            raise forms.ValidationError('county cannot be None')
        
        return rd.date()
    
    def format_manufacture_type(self, val):
        if not val:
            return None
        try:
            return ManufacturingMethod.objects.get(slug=val)
        except ManufacturingMethod.DoesNotExist:
            raise Exception('ManufacturingMethod not found: %s' % val) 
            
    def clean_onepot(self):
        onepot = self.cleaned_data.get('onepot', False)
        if onepot is True:
            return self.format_manufacture_type('onepot')
        return self.format_manufacture_type('not-specified')
        
    #    def clean_onepot(self):
    #        onepot = self.cleaned_data.get('onepot', False)
    #        if onepot is True:
    #            return self.format_manufacture_type('onepot')
    #        return None


        
    def clean_county(self):
        county = self.cleaned_data.get('county', None)
        if county is None:
            raise forms.ValidationError('county cannot be None')
        
        idx = county.find('(')
        if idx > -1:
            county = county[:idx].strip()
            
        return county

    def get_formatted_data(self):
        pass
        
#
"""
with open('ISP_Meth_Lab_Locations_Table.csv', 'rb') as csvfile:
     methreader = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in methreader:
         print ('-'*40)
         print ('--'.join(row))
"""
'''
from __future__ import print_function
from os.path import join, dirname, abspath
import xlrd

fname = 'ISP_Meth_Lab_Locations_Table.xls'
#fname = join(dirname(dirname(abspath(__file__))), 'test_data', 'Cad Data Mar 2014.xlsx')

# Open the workbook
xl_workbook = xlrd.open_workbook(fname)

# List sheet names, and pull a sheet by name
#
sheet_names = xl_workbook.sheet_names()
print('Sheet Names', sheet_names)

xl_sheet = xl_workbook.sheet_by_name(sheet_names[0])

# Or grab the first sheet by index 
#  (sheets are zero-indexed)
#
xl_sheet = xl_workbook.sheet_by_index(0)
print ('Sheet name: %s' % xl_sheet.name)

# Pull the first row by index
#  (rows/columns are also zero-indexed)
#
row = xl_sheet.row(0)  # 1st row

# Print 1st row values and types
#
from xlrd.sheet import ctype_text   

print('(Column #) type:value')
for idx, cell_obj in enumerate(row):
    cell_type_str = ctype_text.get(cell_obj.ctype, 'unknown type')
    print('(%s) %s %s' % (idx, cell_type_str, cell_obj.value))

# Print all values, iterating through rows and columns
#
num_cols = xl_sheet.ncols   # Number of columns
for row_idx in range(0, xl_sheet.nrows):    # Iterate through rows
    print ('-'*40)
    print ('Row: %s' % row_idx)   # Print row number
    for col_idx in range(0, num_cols):  # Iterate through columns
        cell_obj = xl_sheet.cell(row_idx, col_idx)  # Get cell object by row, col
        print cell_obj.type
        #print ('Column: [%s] cell_obj: [%s]' % (col_idx, cell_obj))
    break

'''