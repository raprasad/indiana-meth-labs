from __future__ import print_function

from os.path import abspath, dirname, join, isfile

if __name__=='__main__':
    import os, sys
    REPOSITORY_DIR = dirname(dirname(abspath(__file__)))
    print ('REPOSITORY_DIR', REPOSITORY_DIR)
    sys.path.append(join(REPOSITORY_DIR, 'methlabs'))
    sys.path.append(join(REPOSITORY_DIR, 'methlabs', 'methlabs'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "methlabs.settings.local")

from django.conf import settings
from apps.clanlabs_importer.forms_import import MethImportForm
import csv

def format_boolean(val):
    if val in ('true', 'false'):
        return eval(val.title())
    return val
    
    
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
                
if __name__=='__main__':
    fname = join('meth_data', 'ISP_Meth_Lab_Locations_Table.csv')
    test_run(fname)