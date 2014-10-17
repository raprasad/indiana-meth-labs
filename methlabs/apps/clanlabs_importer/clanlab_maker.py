import csv

from apps.counties.models import County
from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod, ClandestineLabReport, MANUFACTURING_METHOD_NOT_SPECIFIED_SLUG

from apps.clanlabs.forms import ClandestineLabReportForm

from apps.clanlabs_importer.forms_import import MethImportForm

    

class ClandestineLabCSVImporter:
    
    def __init__(self, csv_input_fname, start_row=1, stop_row=10000000):
        assert isfile(csv_input_fname) is True, "File not found: %s" % csv_input_fname
        assert (stop_row >= stop_row)
        self.csv_input_fname = csv_input_fname
        
    def proocess_csv_file(self):
        
        field_names =  MethImportForm.base_fields.keys()

        with open(self.csv_input_fname, 'rb') as csvfile:
            methreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row_cnt, clanlab_info_row in enumerate(methreader, start=1):
                if row_cnt==1: 
                    continue    # skip header row
                
                if row_cnt < self.start_row: continue
                if row_cnt > self.stop_row: break

                # Create a dict with attribute names/values
                meth_info_dict = dict(zip(field_names, clanlab_info_row))
                
                # Use form to validate/transform
                check_csv_form = MethImportForm(meth_info_dict)

                if not check_csv_form.is_valid():
                    print ('NOPE! Failure on line')
                    continue
                    
                clanlab_form = ClandestineLabReportForm(check_csv_form.get_formatted_dict())
                if clanlab_form.is_valid():
                    for k, v in clanlab_form.cleaned_data.items:
                        print ('%s: %s' % (k,v))
                else:
                    print ('NOPE! Failure of form!!')
                
                
def test_run(fname):
    assert isfile(fname) is True, "File not found: %s" % fname
    field_names =  MethImportForm.base_fields.keys()
    with open(fname, 'rb') as csvfile:
        methreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row_cnt, row in enumerate(methreader, start=1):
            if row_cnt==1: 
                continue    # skip header row
            #row = [format_boolean(val) for val in row]
            meth_info_dict = dict(zip(field_names, row))
            print ('-' * 60)
            print ('------------------ INPUT ----------------------')
            
            print(meth_info_dict)
            f = MethImportForm(meth_info_dict)
            if not f.is_valid():
                print (f.errors)
                break
            print ('------------------ CLEAN ----------------------')
            for k,v in f.cleaned_data.items():
                if not v: continue
                print ('%s: %s' % (k,v))
                #if k=='onepot':sys.exit(0)
            #print (f.cleaned_data)
            print ('f.get_final_manufacture_method_type: -%s-' % f.get_final_manufacture_method_type())
            print ('f.get_final_seizure_location_type: %s' % f.get_final_seizure_location_type())
            if row_cnt==5:
                break
