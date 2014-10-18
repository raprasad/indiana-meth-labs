from os.path import isfile
import csv

from apps.utils.msg_util import * 
from apps.counties.models import County
from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod, ClandestineLabReport

from apps.clanlabs.forms import ClandestineLabReportForm

from apps.clanlabs_importer.forms_import import MethImportForm


class ClandestineLabCSVImporter:
    
    def __init__(self, csv_input_fname, start_row=1, stop_row=10000000):
        assert isfile(csv_input_fname) is True, "File not found: %s" % csv_input_fname
        assert type(start_row) is int, "start_row must be an integer.  Found type: %s" % type(start_row)
        assert type(stop_row) is int, "stop_row must be an integer.  Found type: %s" % type(stop_row)
        assert (start_row <= stop_row)
        
        self.csv_input_fname = csv_input_fname
        self.start_row = start_row
        self.stop_row = stop_row
        
    def process_csv_file(self):
        
        field_names =  MethImportForm.base_fields.keys()

        with open(self.csv_input_fname, 'rb') as csvfile:
            methreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row_cnt, clanlab_info_row in enumerate(methreader, start=1):
                msgt('(%s) processing row' % row_cnt)
                if row_cnt==1: 
                    continue    # skip header row
                
                # Only process specific rows
                if row_cnt < self.start_row: continue
                if row_cnt > self.stop_row: break

                # Create a dict with attribute names/values
                meth_info_dict = dict(zip(field_names, clanlab_info_row))
                
                # Use form to validate/transform
                check_csv_form = MethImportForm(meth_info_dict)

                if not check_csv_form.is_valid():
                    print ('NOPE! Failure on line')
                    print (check_csv_form.errors)
                    break
                    
                csv_formatted_info = check_csv_form.get_formatted_dict()     
                    
                clanlab_form = ClandestineLabReportForm(csv_formatted_info)
                if clanlab_form.is_valid():
                    msgt('cleaned final form')
                    for k, v in clanlab_form.cleaned_data.items():
                        print ('%s: %s' % (k,v))
                    
                    # Is it already in the db?
                    if ClandestineLabReport.objects.filter(**clanlab_form.cleaned_data).count() > 0:
                        msg('----------> Already exists!  :)\n')
                        continue
                    
                    #---------------------
                    # Make a new lab
                    #---------------------
                    clanlab_obj = ClandestineLabReport(**clanlab_form.cleaned_data)
                    clanlab_obj.save()

                    #---------------------
                    # Add location types
                    #---------------------
                    for slt in csv_formatted_info['seizure_location_type_ids']:
                        clanlab_obj.seizure_location_types.add(slt)
                    clanlab_obj.save()
                    
                    #---------------------
                    # Add manufacturing methods
                    #---------------------
                    for mmt in csv_formatted_info['manufacture_method_type_ids']:
                        clanlab_obj.manufacturing_methods.add(mmt)
                    clanlab_obj.save()
                    
                    
                    msg('clanlab_obj saved: %s' % clanlab_obj.id)
                else:
                    msgt('meth_info_dict')
                    
                    for k, v in meth_info_dict.items(): 
                        print ('%s: %s' % (k,v))
                    print ('NOPE! Failure of form!!')
                    print (clanlab_form.errors)
                    for field, errors in clanlab_form.errors.items():
                        print '-'
                        print 'Field: %s' % field
                        for err in errors:
                            print 'err: %s' % err
                        #print 'Errors: %s' % errors
                    break
                
