from django import forms
from brubeck.models import CartItem

class ProductAddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ('quantity',)

    quantity = forms.IntegerField(widget=forms.TextInput(attrs={'size':'2', 'value':'1', 'class':'quantity'}), 
                                  error_messages={'invalid':'Please enter a valid quantity.'}, 
                                  min_value=1)
    