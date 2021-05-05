from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    #coerce=int to convert input into int of quantity
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
    #hidden input widget to not to show this to user
