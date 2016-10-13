from ecomstore.billing.models import Card
from django import forms
from datetime import datetime

month_choice = []
# month_choice.append(('','- Month -'))
for i in range(1,13):
    if len(str(i)) == 1:
        numeric = '0' + str(i)
    else:
        numeric = str(i)
    month_choice.append((numeric, datetime(2009, i, 1).strftime('%B')))
MONTHS = tuple(month_choice)


calendar_years = []
# calendar_years.append(('','- Year -'))
for i in range(datetime.now().year, datetime.now().year+10):
    calendar_years.append((i,i))
YEARS = tuple(calendar_years)

class CardForm(forms.ModelForm):
    CARD_TYPES = (('Visa', 'Visa'),
                ('Amex', 'Amex'),
                ('Discover', 'Discover'),
                ('Mastercard', 'Mastercard'),)
    class Meta:
        model = Card
        exclude = ('data','num', 'user')
       
    cardholder_name = forms.CharField(max_length=100)
    card_number = forms.CharField(max_length=20)
    card_type = forms.ChoiceField(choices=CARD_TYPES)
    card_expire_month = forms.ChoiceField(choices=MONTHS)
    card_expire_year = forms.ChoiceField(choices=YEARS)