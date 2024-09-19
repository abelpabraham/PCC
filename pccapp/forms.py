from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from .models import Product, PaperType, ProductSize, PaperThickness, PaperSize, PaperConfiguration, Substrate, SubstrateSize, SubstrateThickness, SubstrateConfiguration


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'cost_per_unit', 'uom', 'min_quantity']
        widgets = {
            'name': forms.TextInput(attrs= {'class': 'form-control'}),
            'cost_per_unit': forms.NumberInput(attrs= {'class': 'form-control', 'step': '0.01'}),
            'uom': forms.Select(attrs= {'class': 'form-control'}),
            'min_quantity': forms.NumberInput(attrs= {'class': 'form-control'})
        }
        
class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'cost_per_unit']

class PaperTypeForm(forms.ModelForm):
    class Meta:
        model = PaperType
        fields = ['name', 'cost_per_unit']

class ProductSizeForm(forms.ModelForm):
    class Meta:
        model = ProductSize
        fields = ['product', 'width', 'height', 'cost_adjustment']

class PaperThicknessForm(forms.ModelForm):
    class Meta:
        model = PaperThickness
        fields = ['gsm', 'cost_adjustment']

class PaperSizeForm(forms.ModelForm):
    class Meta:
        model = PaperSize
        fields = ['name', 'width', 'height', 'cost_adjustment']

class PaperConfigurationForm(forms.ModelForm):
    class Meta:
        model = PaperConfiguration
        fields = ['paper_type', 'paper_size', 'paper_thickness']

class SubstrateForm(forms.ModelForm):
    class Meta:
        model = Substrate
        fields = ['name', 'base_cost_per_unit']

class SubstrateSizeForm(forms.ModelForm):
    class Meta:
        model = SubstrateSize
        fields = ['width', 'height', 'cost_adjustment']

class SubstrateThicknessForm(forms.ModelForm):
    class Meta:
        model = SubstrateThickness
        fields = ['thickness_value', 'cost_adjustment']

class SubstrateConfigurationForm(forms.ModelForm):
    class Meta:
        model = SubstrateConfiguration
        fields = ['substrate', 'substrate_size', 'substrate_thickness']


class ProductPaperSpecificationForm(forms.Form):
    product_size = forms.ModelChoiceField(
        queryset=ProductSize.objects.none(),
        label="Select Product Size",
        required=True
    )
    paper_size = forms.ModelChoiceField(
        queryset=PaperSize.objects.all(),
        label="Select Paper Size",
        required=True
    )

    def __init__(self, *args, **kwargs):
        product_id = kwargs.pop('product_id', None)  
        super(ProductPaperSpecificationForm, self).__init__(*args, **kwargs)
        
        if product_id:
            self.fields['product_size'].queryset = ProductSize.objects.filter(product_id=product_id)
