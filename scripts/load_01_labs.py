from __future__ import print_function

from os.path import abspath, dirname, join, isfile

if __name__=='__main__':
    import os, sys
    REPOSITORY_DIR = dirname(dirname(abspath(__file__)))
    #print ('REPOSITORY_DIR', REPOSITORY_DIR)
    sys.path.append(join(REPOSITORY_DIR, 'methlabs'))
    sys.path.append(join(REPOSITORY_DIR, 'methlabs', 'methlabs'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "methlabs.settings.local")

from django.conf import settings
from apps.clanlabs_importer.clanlab_maker import ClandestineLabCSVImporter


def run_csv_import(csv_fname, start_row=0, stop_row=100000):
                
    csv_importer = ClandestineLabCSVImporter(csv_fname, start_row, stop_row)
    csv_importer.process_csv_file()
    
if __name__=='__main__':
    fname = join('meth_data', 'ISP_Meth_Lab_Locations_Table.csv')
    run_csv_import(fname, start_row=8419, stop_row=98420)