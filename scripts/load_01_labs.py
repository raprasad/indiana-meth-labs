from __future__ import print_function

from os.path import abspath, dirname, join, isfile

if __name__=='__main__':
    import os, sys
    REPOSITORY_DIR = dirname(dirname(abspath(__file__)))
    print ('REPOSITORY_DIR', REPOSITORY_DIR)
    sys.path.append(join(REPOSITORY_DIR, 'methlabs'))
    sys.path.append(join(REPOSITORY_DIR, 'methlabs', 'methlabs'))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "methlabs.settings.local")

import xlrd
from django.conf import settings
from apps.counties.models import County


column_headers = ('report_date', 'county', 'location', 'vin_number', 'pdf_report', 'clean_cert', 'case_number', 'lab_number', 'residence', 'outbuilding', 'vehicle', 'hotel_motel', 'open', 'business', 'other', 'red_p', 'nazi', 'onepot') 

def load_books(datafile, start_row=1, end_row=200):
    
    if not os.path.isfile(datafile):
        raise Exception('This file does not exist! %s' % datafile)

    authors = []
    with open(datafile, 'rb') as csvfile:
        dataset_reader = csv.reader(csvfile, delimiter=';', quotechar='"')
        cnt = 0
        for row in dataset_reader:
            cnt +=1
            if cnt==1: continue # skip header row
            if cnt < start_row: continue
            if cnt > end_row: break
            
            d = dict(zip(book_attributes, row))
            print ('(%s) %s' % (cnt, d))
            
            author_name = d['author'].decode('utf-8')
            
            
            name_parts = author_name.split()
            if len(name_parts) in [2, 3] and author_name.find(',') == -1:
                first_name = name_parts[0]
                last_name = name_parts[-1]
                if len(name_parts) == 3:
                    middle_name = name_parts[1]
                else:
                    middle_name = ''
                    
                author_dict = dict(first_name=first_name\
                                    , last_name=last_name\
                                    , middle_name=middle_name\
                                    )
                print ('author_dict', author_dict)
                # does author exist
                if Author.objects.filter(**author_dict).count() > 0:
                    continue
                
                # add author
                author = Author(**author_dict)
                author.save()
                print ('new author saved: %s' %  author)
                
                authors.append(author)
                
            # create a user 
            #name_parts = d['author'].split()
            #fname = name_parts[0]
            #lname = name_parts[-1]
            #username = '%s_%s' % 

            #print (d)
            #    self.datasets.append(new_ds)
            #    print('(%s) added: %s' % (cnt, new_ds.title))
    
    author_set = set(authors)
    print (author_set)
    print (len(author_set))
    
    
if __name__=='__main__':
    fname = join('meth_data', 'ISP_Meth_Lab_Locations_Table.xls')
    