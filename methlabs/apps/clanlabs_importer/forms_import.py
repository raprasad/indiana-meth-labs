from __future__ import print_function
from django import forms

from apps.counties.models import County
from apps.clanlabs.models import SeizureLocationType, ManufacturingMethod, MANUFACTURING_METHOD_NOT_SPECIFIED_SLUG


MANUFACTURE_TYPE_ATTRIBUTES = ('red_p', 'nazi', 'onepot')
SEIZURE_LOCATION_TYPE_ATTRIBUTES = ('residence', 'outbuilding', 'vehicle', 'hotel_or_motel', 'open_area', 'business', 'other')
# (yes, we can dynamically create the form attributes from the lists above, but want to be verbose for demo)

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
    
    def clean_case_number(self):
        val = self.cleaned_data.get('case_number', None)
        
        if not val: # None or ''
            return 
        
    #------------------------------------
    #   Manufacture Type
    #------------------------------------    
    def get_manufacture_type(self, attribute_name):
        """
        If the manufacture type is 'True', return the related ManufacturingMethod object
        """
        assert attribute_name is not None, "attribute_name cannot be None"
        
        is_checked = self.cleaned_data.get(attribute_name, False)
        
        if is_checked is False:
            return None
            
        try:
            return ManufacturingMethod.objects.get(slug=attribute_name)
        except ManufacturingMethod.DoesNotExist:
            raise Exception('ManufacturingMethod not found: %s' % attribute_name) 
                
    
    def clean_onepot(self):
        """Convert a value of True to the appropriate ManufacturingMethod object"""
        return self.get_manufacture_type('onepot')
        
    def clean_nazi(self):
        """Convert a value of True to the appropriate ManufacturingMethod object"""
        return self.get_manufacture_type('onepot')

    def clean_red_p(self):
        """Convert a value of True to the appropriate ManufacturingMethod object"""
        return self.get_manufacture_type('red_p')


    def get_final_manufacture_method_type(self):
         """
         Return a ManufacturingMethod object used to create a ClandestineLabReport object

         Either return one of the ManufacturingMethods from the spreadsheet or the 'Not Specified' object
         """
         for key in MANUFACTURE_TYPE_ATTRIBUTES:
             if self.cleaned_data.get(key, None) is not None:
                 return self.cleaned_data[key]
         try:        
             return ManufacturingMethod.objects.get(slug=MANUFACTURING_METHOD_NOT_SPECIFIED_SLUG)
         except ManufacturingMethod.DoesNotExist:
             raise Exception('ManufacturingMethod not found: %s' % MANUFACTURING_METHOD_NOT_SPECIFIED_SLUG)


    #------------------------------------
    #   Seizure Location Type
    #------------------------------------    

    def get_seizure_location_type(self, attribute_name):
        """
        If the seizure location type is 'True', return the related SeizureLocationType object
        """
        assert attribute_name is not None, "attribute_name cannot be None"
        
        is_checked = self.cleaned_data.get(attribute_name, False)

        if is_checked is True:
            slug_name = attribute_name.replace('_', '-')
            try:
                return SeizureLocationType.objects.get(slug=slug_name)
            except SeizureLocationType.DoesNotExist:
                raise Exception('SeizureLocationType not found: %s' % attribute_name) 
        return None


    def clean_residence(self):
        """Convert a value of True to the appropriate SeizureLocationType object"""
        return self.get_seizure_location_type('residence')

    def clean_outbuilding(self):
        """Convert a value of True to the appropriate SeizureLocationType object"""
        return self.get_seizure_location_type('outbuilding')

    def clean_vehicle(self):
        """Convert a value of True to the appropriate SeizureLocationType object"""
        return self.get_seizure_location_type('vehicle')

    def clean_hotel_or_motel(self):
        """Convert a value of True to the appropriate SeizureLocationType object"""
        return self.get_seizure_location_type('hotel_or_motel')

    def clean_open_area(self):
        """Convert a value of True to the appropriate SeizureLocationType object"""
        return self.get_seizure_location_type('open_area')

    def clean_business(self):
        """Convert a value of True to the appropriate SeizureLocationType object"""
        return self.get_seizure_location_type('business')

    def clean_other(self):
        """Convert a value of True to the appropriate SeizureLocationType object"""
        return self.get_seizure_location_type('other')


    def get_final_seizure_location_types(self):
        """
        Return a list of SeizureLocationType objects used to create a ClandestineLabReport object

        The list may have 0, 1 or several SeizureLocationType objects
        """
        location_types = []
        for key in SEIZURE_LOCATION_TYPE_ATTRIBUTES:
            if self.cleaned_data.get(key, None) is not None:
                location_types.append(self.cleaned_data[key])
        return location_types

    
    #------------------------------------
    # Clean county information
    #------------------------------------
    def clean_county(self):
        """
        Return an existing County object or create a new one
        
        Format the value:  e.g. "Hamilton (29)" becomes "Hamilton"
        """
        county = self.cleaned_data.get('county', None)
        if county is None:
            raise forms.ValidationError('county cannot be None')
        
        idx = county.find('(')
        if idx > -1:
            county = county[:idx].strip()
        
        try:
            county_obj = County.objects.get(name=county)
        except County.DoesNotExist:
            county_obj = County(name=county)
            county_obj.save()
        return county_obj


    def clean_location(self):
        """
        The locations have 3 lines
            (1) address line
            (2) city, state
            (3) lat, lng
        
        Example:     
            Sauerkraut Ln
            Mt. Vernon, IN
            (37.94020019600049, -87.93726333199965)

        Return a tuple with these components
        """
        location_info = self.cleaned_data('location', None)
        if county is None:
            raise forms.ValidationError('location cannot be None')
        
        location_lines = location_info.split('\n')
        if not len(location_lines) == 3:
            raise forms.ValidationError('The location should have 3 lines')
        
        location_lines = [ line.strip() for x in location_lines]
        
        return tuple(location_lines)
        

    def get_formatted_dict(self):
        assert self.cleaned_data is not None, "Only call this after form has been successfully validated"
            
        fmt_dict = {}
        fmt_dict.update({self.cleaned_data})
        
        fmt_dict['manufacture_method'] = self.get_final_manufacture_method_type()
        fmt_dict['seizure_location_types'] = self.get_final_seizure_location_types()
        fmt_dict['address'] = ', '.join(self.clean_location()[:2])
        
        lat, lng = eval(self.clean_location()[-1])
        fmt_dict['lat_position'] = lat
        fmt_dict['lng_position'] = lng

        return fmt_dict
        
"""
with open('ISP_Meth_Lab_Locations_Table.csv', 'rb') as csvfile:
     methreader = csv.reader(csvfile, delimiter=',', quotechar='"')
     for row in methreader:
         print ('-'*40)
         print ('--'.join(row))
"""
