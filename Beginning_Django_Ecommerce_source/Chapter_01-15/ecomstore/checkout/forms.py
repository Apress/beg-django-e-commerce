from django import forms
from ecomstore.checkout.models import Order
from ecomstore.settings import DEBUG
import datetime
import re

def cc_expire_years():
    """ list of years starting with current twelve years into the future """
    current_year = datetime.datetime.now().year
    years = range(current_year, current_year+12)
    return [(str(x),str(x)) for x in years]

def cc_expire_months():
    """ list of tuples containing months of the year for use in credit card form.
    [('01','January'), ('02','February'), ... ]
    
    """
    months = []
    for month in range(1,13):
        if len(str(month)) == 1:
            numeric = '0' + str(month)
        else:
            numeric = str(month)
        months.append((numeric, datetime.date(2009, month, 1).strftime('%B')))
    return months

CARD_TYPES = (('Mastercard','Mastercard'),
             ('VISA','VISA'),
             ('AMEX','AMEX'),
             ('Discover','Discover'),)

def strip_non_numbers(data):
    """ gets rid of all non-number characters """
    non_numbers = re.compile('\D')
    return non_numbers.sub('', data)
    

def cardLuhnChecksumIsValid(card_number):
    """ checks to make sure that the card passes a Luhn mod-10 checksum 
    Taken from: http://code.activestate.com/recipes/172845/
    
    """
    sum = 0
    num_digits = len(card_number)
    oddeven = num_digits & 1
    for count in range(0, num_digits):
        digit = int(card_number[count])
        if not (( count & 1 ) ^ oddeven ):
            digit = digit * 2
        if digit > 9:
            digit = digit - 9
        sum = sum + digit
    return ( (sum % 10) == 0 )

class CheckoutForm(forms.ModelForm):
    """ checkout form class to collect user billing and shipping information for placing an order """
    def __init__(self, *args, **kwargs):
        super(CheckoutForm, self).__init__(*args, **kwargs)
        # override default attributes
        for field in self.fields:
            self.fields[field].widget.attrs['size'] = '30'
            
        self.fields['shipping_state'].widget.attrs['size'] = '3'
        self.fields['shipping_state'].widget.attrs['size'] = '3'
        self.fields['shipping_zip'].widget.attrs['size'] = '6'
        
        self.fields['billing_state'].widget.attrs['size'] = '3'
        self.fields['billing_state'].widget.attrs['size'] = '3'
        self.fields['billing_zip'].widget.attrs['size'] = '6'
        
        self.fields['credit_card_type'].widget.attrs['size'] = '1'
        self.fields['credit_card_expire_year'].widget.attrs['size'] = '1'
        self.fields['credit_card_expire_month'].widget.attrs['size'] = '1'
        self.fields['credit_card_cvv'].widget.attrs['size'] = '5'
        
    class Meta:
        model = Order
        exclude = ('status','ip_address','user','transaction_id',)
        
    credit_card_number = forms.CharField()
    credit_card_type = forms.CharField(widget=forms.Select(choices=CARD_TYPES))
    credit_card_expire_month = forms.CharField(widget=forms.Select(choices=cc_expire_months()))
    credit_card_expire_year = forms.CharField(widget=forms.Select(choices=cc_expire_years()))
    credit_card_cvv = forms.CharField()
    
    def clean_credit_card_number(self):
        """ validate credit card number if valid per Luhn algorithm """
        cc_number = self.cleaned_data['credit_card_number']
        stripped_cc_number = strip_non_numbers(cc_number)
        if not cardLuhnChecksumIsValid(stripped_cc_number):
            raise forms.ValidationError('The credit card you entered is invalid.')
        
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        stripped_phone = strip_non_numbers(phone)
        if len(stripped_phone) < 10:
            raise forms.ValidationError('Enter a valid phone number with area code.(e.g. 555-555-5555)')
        return self.cleaned_data['phone']
