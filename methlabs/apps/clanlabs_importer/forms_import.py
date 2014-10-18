from __future__ import print_function
from django import forms

from apps.utils.msg_util import * 

from apps.counties.models import County, Town
from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod\
                , CASE_NUMBER_NOT_AVAILABLE


MANUFACTURE_TYPE_ATTRIBUTES = ('red_p', 'nazi', 'onepot')
SEIZURE_LOCATION_TYPE_ATTRIBUTES = ('residence', 'outbuilding', 'vehicle', 'hotel_or_motel', 'open_area', 'business', 'other')
# (yes, we can dynamically create the form attributes from the lists above, but want to be verbose for demo)

class MethImportForm(forms.Form):
    """Used to read CSV file with Meth Data"""
    
    report_date = forms.DateTimeField(input_formats=['%m/%d/%Y %H:%M:%S AM', '%m/%d/%Y %H:%M:%S PM'])
    county = forms.CharField(max_length=100)
    location = forms.CharField(label='address, lat, lng')

    vin_number = forms.CharField(max_length=100, required=False)
    pdf_report_link = forms.URLField(max_length=255, required=False)
    clean_cert = forms.CharField(max_length=100, required=False)
    
    case_number = forms.CharField(max_length=70, required=False)
    lab_number = forms.CharField(max_length=255, required=False)

    # seizure location
    residence = forms.BooleanField(required=False)
    outbuilding = forms.BooleanField(required=False)
    vehicle = forms.BooleanField(required=False)
    hotel_or_motel = forms.BooleanField(required=False)
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
 
    #------------------------------------
    #   Manufacture Type
    #------------------------------------    
    def get_final_manufacture_method_type_ids(self):
        """
        Return a ManufacturingMethod object used to create a ClandestineLabReport object

        Either return one of the ManufacturingMethods from the spreadsheet or the 'Not Specified' object
        """
        manufacture_method_ids = []
        for manufacture_type_attr in MANUFACTURE_TYPE_ATTRIBUTES:
            if self.cleaned_data.get(manufacture_type_attr, False) is True:
                manufacture_type_slug = manufacture_type_attr.replace('_', '-')
                try:
                    manufacture_type = ManufacturingMethod.objects.get(slug=manufacture_type_slug)
                    manufacture_method_ids.append(manufacture_type.id)
                except ManufacturingMethod.DoesNotExist:
                    raise Exception('ManufacturingMethod not found: %s' % manufacture_type_slug)
        return manufacture_method_ids
        
    #------------------------------------
    #   Seizure Location Type
    #------------------------------------    
    def get_seizure_location_type(self, attribute_name):
        """
        If the seizure location type is 'True', return the related SeizureLocationType object
        """
        assert attribute_name is not None, "attribute_name cannot be None"
        
        slug_name = attribute_name.replace('_', '-')
        try:
            return SeizureLocationType.objects.get(slug=slug_name)
        except SeizureLocationType.DoesNotExist:
            raise Exception('SeizureLocationType not found: %s' % attribute_name) 
        
    def get_final_seizure_location_type_ids(self):
        """
        Return a list of SeizureLocationType objects used to create a ClandestineLabReport object

        The list may have 0, 1 or several SeizureLocationType objects
        """
        location_types = []
        for attribute_name in SEIZURE_LOCATION_TYPE_ATTRIBUTES:
            if self.cleaned_data.get(attribute_name, False) is True:
                location_type = self.get_seizure_location_type(attribute_name)
                location_types.append(location_type.id)
        return location_types

    
    #------------------------------------
    # Clean county information
    #------------------------------------
    def clean_county(self):
        """
        (1) Format the county name:  e.g. "Hamilton (29)" becomes "Hamilton"
        (2) Try to look up the County object in the database
        (3) If the County object doesn't exist, then create it 
        (4) Return the County object 'id'
        """
        county = self.cleaned_data.get('county', None)
        if county is None:
            raise forms.ValidationError('county cannot be None')
        
        # (1) Format the county name:  e.g. "Hamilton (29)" becomes "Hamilton"
        idx = county.find('(')
        if idx > -1:
            county = county[:idx].strip()
        
        
        # (2) Try to look up the County object
        try:
            county_obj = County.objects.get(name=county)
        except County.DoesNotExist:
            # (3) the County object doesn't exist, create it
            county_obj = County(name=county)
            county_obj.save()

        # (4) Return the county id
        return county_obj.id


    def clean_location(self):
        """
        The locations fields have 3 lines
            (1) address line
            (2) city, state
            (3) lat, lng

        These are converted to tuples automatically

        CSV Address:     

            7887 S CR 200 E
            Portland, IN
            (40.32285454300046, -84.93889686799969)
        Cleaned field:
            (u'7887 S CR 200 E', u'Portland, IN', u'(40.32285454300046, -84.93889686799969)')

        Return a tuple with these components
        """
        location_info = self.cleaned_data.get('location', None)
        print ('location_info', location_info)
        print ('location_info type 1: %s' % type(location_info))
        if location_info is None:
            raise forms.ValidationError('location cannot be None')
        
        # split into a list of lines
        location_lines = location_info.split('\n')

        # trim whitespace from each line
        location_lines = [ x.strip() for x in location_lines]

        # only keep lines with values
        location_lines = filter(lambda x: len(x) > 0, location_lines)
        
        if not len(location_lines) in (2, 3):
            raise forms.ValidationError('The location should have 2 or 3 lines')
        
        
        return tuple(location_lines)
        
    def clean_case_number(self):
        case_number = self.cleaned_data.get('case_number', None)
        if not case_number:
            return CASE_NUMBER_NOT_AVAILABLE
            
        return case_number
    
    def get_town_object_id(self, town_state_str, county_id):
        """
        From a string and county get a Town object
        
        e.g. "Vincennes, IN""
        """
        assert type(county_id) is int
        
        town_parts = town_state_str.split(',')
        msg('town_parts: %s' % town_parts)
        if len(town_parts) == 1:
            town_name = town_parts[0]
        else:
            town_name = ', '.join(town_parts[:-1])  # trim off ", IN"
        
        town_name = town_name.strip()
        if town_name == '':
            raise ValueError('Town name is blank: %s' % town_state_str)
        
        
        try:
            town_obj = Town.objects.get(name=town_name, county_id=county_id)
        except Town.DoesNotExist:
            town_obj = Town(name=town_name, county_id=county_id)
            town_obj.save()
            
        return town_obj.id
        
        
    def get_formatted_dict(self):
        assert self.cleaned_data is not None, "Only call this after form has been successfully validated"
            
        fmt_dict = {}
        fmt_dict.update(self.cleaned_data)
        
        fmt_dict['manufacture_method_type_ids'] = self.get_final_manufacture_method_type_ids()
        fmt_dict['seizure_location_type_ids'] = self.get_final_seizure_location_type_ids()
        fmt_dict['address'] = fmt_dict['location'][0]
        fmt_dict['town'] = self.get_town_object_id(fmt_dict['location'][1], fmt_dict['county']) 
        # e.g. Vincennes, In -> Town object 
        
        # add lat, lng
        if len(fmt_dict['location']) == 3:
            lat, lng = eval(fmt_dict['location'][-1])
            fmt_dict['lat_position'] = lat
            fmt_dict['lng_position'] = lng

        return fmt_dict
