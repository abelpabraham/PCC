from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from . models import *
from . forms import *
from .utils import validate_calculator_form, get_selected_objects, calculate_cost_details,calculate_products_per_sheet
from .decorators import unauthenticated_user, allowed_users, admin_only


# Create your views here.


def landing(request):
    return render(request, 'landing.html')

@unauthenticated_user
def signin(request):    
    if request.method == 'POST':
        email = request.POST.get('email')  
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user with this email found.')
            return render(request, 'index.html')

        user = authenticate(request, username=user.username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('../dashboard')
        else:
            messages.error(request, 'Incorrect email or password.')        
    
    return render(request, 'index.html')


def logoutUser(request):
    logout(request)
    return redirect('landing')

def custom_page_not_found(request, exception):
    return render(request, '404.html', {}, status=404)

@login_required(login_url='signin')
@admin_only
def dashboard(request):
    
    today = timezone.now().date()
    todays_calculations = CalculationRecord.objects.filter(time__date = today)
    context = {
        'tc': todays_calculations,
    }
    return render(request, 'Ad_user/dashboard.html', context)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['guest'])
def userhome(request):
    return render(request, 'Gen_user/dashboard.html')


@login_required(login_url='signin')
def productview(request):
    prod=Product.objects.all()
    if request.user.groups.filter(name='admin').exists():
        return render(request, 'Ad_user/product.html', {'product': prod})
        
    elif request.user.groups.filter(name='guest').exists():
        return render(request, 'Gen_user/product.html', {'product': prod})
    
    
@login_required(login_url='signin')
def product_sizeview(request):
    size=ProductSize.objects.all()
    if request.user.groups.filter(name='admin').exists():
        return render(request, 'Ad_user/productsize.html', {'size':size})
        
    elif request.user.groups.filter(name='guest').exists():
        return render(request, 'Gen_user/productsize.html', {'size':size})


@login_required(login_url='signin')
def paper_sizeview(request):
    size=PaperSize.objects.all()
    if request.user.groups.filter(name='admin').exists():
        return render(request, 'Ad_user/papersize.html', {'size':size})
    elif request.user.groups.filter(name='guest').exists():
            return render(request, 'Gen_user/papersize.html', {'size':size})


@login_required(login_url='signin')
def paper_configuration(request):
    conf=PaperConfiguration.objects.all()
    if request.user.groups.filter(name='admin').exists():
        return render(request, 'Ad_user/paper_conf.html', {'conf':conf})
    elif request.user.groups.filter(name='guest').exists():
            return render(request, 'Gen_user/paper_conf.html', {'conf':conf})


@login_required(login_url='signin')
def substrateview(request):
    sub=Substrate.objects.all()
    if request.user.groups.filter(name='admin').exists():
        return render(request, 'Ad_user/substrate.html', {'sub':sub})
    elif request.user.groups.filter(name='guest').exists():
            return render (request, 'Gen_user/substrate.html', {'sub':sub})


@login_required(login_url='signin')
def susbtrate_sizeview(request):
    size=SubstrateSize.objects.all()
    if request.user.groups.filter(name='admin').exists():
        return render(request, 'Ad_user/substrate_size.html', {'size':size})
    elif request.user.groups.filter(name='guest').exists():
            return render (request, 'Gen_user/substrate_size.html', {'size':size})


@login_required(login_url='signin')
def susbtrate_thicknessview(request):
    thick=SubstrateThickness.objects.all()
    if request.user.groups.filter(name='admin').exists():
        return render(request, 'Ad_user/substrate_thickness.html', {'thick':thick})
    elif request.user.groups.filter(name='guest').exists():
            return render (request, 'Gen_user/substrate_thickness.html', {'thick':thick})


@login_required(login_url='signin')
def substrate_configuration(request):
    conf=SubstrateConfiguration.objects.all()
    if request.user.groups.filter(name='admin').exists():
        return render(request, 'Ad_user/substrate_conf.html', {'conf':conf})
    elif request.user.groups.filter(name='guest').exists():
            return render(request, 'Gen_user/substrate_conf.html', {'conf':conf})


@login_required(login_url='signin')
def productedit(request, product_id):
    instance = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductEditForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('productview')
    else:
        form = ProductForm(instance=instance)
    
    if request.is_ajax():
        return render(request, 'edit_modal.html', {'form': form})
    return render(request, 'edit_modal.html', {'form': form})


@login_required(login_url='signin')
def productsizeedit(request, productsize_id):
    instance = get_object_or_404(ProductSize, id=productsize_id)
    if request.method == 'POST':
        form = ProductSizeForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('productsizeview')
    else:
        form = ProductSizeForm(instance=instance)    
    
    return render(request, 'Ad_user/add_product.html', {'form': form})


@login_required(login_url='signin')
def activateproduct(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.status == 1:
        product.status = 0 
    else:
        product.status = 1 
    product.save()
    
    return redirect('productview')


from .models import CalculationRecord
from django.utils import timezone

@login_required(login_url='signin')
def calculator(request):
    products = Product.objects.all()
    product_sizes = ProductSize.objects.all()
    substrates = Substrate.objects.all()
    substrate_sizes = SubstrateSize.objects.all()
    paper_sizes = PaperSize.objects.all()

    context = {
        'products': products,
        'product_sizes': product_sizes,
        'substrates': substrates,
        'substrate_sizes': substrate_sizes,
        'paper_sizes': paper_sizes,
    }

    if request.method == "POST":
        form_data = request.POST
        errors = validate_calculator_form(form_data)

        if errors:
            context.update({'errors': errors})
            return render(request, 'Ad_user/findcost.html', context)

        selected_product, selected_size, selected_paper_size, selected_substrate, selected_substrate_size = get_selected_objects(
            form_data.get('product'),
            form_data.get('product_size'),
            form_data.get('paper_size_option'),
            form_data.get('substrate'),
            form_data.get('substrate_size')
        )

        quantity = int(form_data.get('quantity'))
        substrate_quantity = int(form_data.get('substrate_quantity') or 0)
        paper_quantity = int(form_data.get('paper_quantity') or 0)
        
        if selected_product.min_quantity and quantity < selected_product.min_quantity:
            errors.append(f"Minimum quantity for '{selected_product.name}' is {selected_product.min_quantity}.")
        
        if errors:
            context.update({'errors': errors})
            return render(request, 'Ad_user/findcost.html', context)

        cost_details = calculate_cost_details(
            selected_product,
            selected_size,
            quantity,
            selected_paper_size,
            selected_substrate,
            selected_substrate_size,
            substrate_quantity,
            paper_quantity
        )

        grand_total = cost_details.get('grand_total')

        CalculationRecord.objects.create(
            user=request.user,
            product=selected_product,
            product_size=selected_size,
            number_of_products=quantity,
            grand_total=grand_total,
        )

        context.update({
            'selected_product': selected_product,
            'selected_size': selected_size,
            'quantity': quantity,
            'substrate_quantity': substrate_quantity,
            'paper_quantity': paper_quantity,
            'cost_details': cost_details,
        })

    if request.user.groups.filter(name='admin').exists():
        return render(request, 'Ad_user/findcost.html', context)
    elif request.user.groups.filter(name='guest').exists():
        return render(request, 'Gen_user/findcost.html', context)



@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def addproduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('dashboard')
    else:
        form=ProductForm
    return render(request,'Ad_user/add_product.html',{'form':form})


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def addpaper(request):
    if request.method == 'POST':
        form = PaperTypeForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('papersizeview')
    else:
        form=ProductForm
    return render(request,'Ad_user/add_product.html',{'form':form})


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def addsubstrate(request):
    if request.method == 'POST':
        form = SubstrateForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('substrateview')
    else:
        form=ProductForm
    return render(request,'Ad_user/add_product.html',{'form':form})


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def deleteproduct(request,product_id):
    data=get_object_or_404(Product,pk=product_id)
    data.delete()
    return redirect('productview') 


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def deleteproduct(request,product_id):
    data=get_object_or_404(Product,pk=product_id)
    data.delete()
    return redirect('productview') 


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def deleteproduct(request,product_id):
    data=get_object_or_404(Product,pk=product_id)
    data.delete()
    return redirect('productview') 


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def deleteproduct(request,product_id):
    data=get_object_or_404(Product,pk=product_id)
    data.delete()
    return redirect('productview') 


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def deletepaperconf(request,paper_id):
    data=get_object_or_404(PaperConfiguration,pk=paper_id)
    data.delete()
    return redirect('paperconfiguration') 

def product_size_and_paper_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    products_per_sheet = None

    if request.method == 'POST':
        form = ProductPaperSpecificationForm(request.POST, product_id=product_id)
        if form.is_valid():
            selected_product_size = form.cleaned_data['product_size']
            selected_paper_size = form.cleaned_data['paper_size']
        products_per_sheet = calculate_products_per_sheet(selected_product_size, selected_paper_size)
            
            
    else:
        form = ProductPaperSpecificationForm(product_id=product_id)

    context = {
        'product': product,
        'form': form,
        'products_per_sheet': products_per_sheet,
    }
    return render(request, 'Gen_user/productspecification.html', context)

