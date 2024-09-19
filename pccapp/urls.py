from django.urls import path
from django.conf.urls import handler404
from . import views

handler404 = 'pccapp.views.custom_page_not_found'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('signin/',views.signin, name='signin'),
    path('logout/',views.logoutUser, name='logout'),    
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('userhome/', views.userhome, name='userhome'),

    
    path('productview/',views.productview,name='productview'),
    path('productsizeview/', views.product_sizeview, name='productsizeview'),
    path('papersizeview/', views.paper_sizeview, name='papersizeview'),
    path('paperconfiguration/', views.paper_configuration, name='paperconfiguration'),    
    path('substrateview/', views.substrateview, name='substrateview'),
    path('susbtrate_sizeview/', views.susbtrate_sizeview, name='susbtrate_sizeview'),
    path('susbtrate_thicknessview/', views.susbtrate_thicknessview, name='susbtrate_thicknessview'),
    path('substrate_configuration/', views.substrate_configuration, name='substrate_configuration'),    
    path('calculator/',views.calculator, name='calculator'),    
    path('product_size_and_paper_view/<int:product_id>/', views.product_size_and_paper_view, name='product_size_and_paper_view'),
    path('productedit/<int:product_id>/', views.productedit, name='productedit'),
    path('productsizeedit/<int:productsize_id>/', views.productsizeedit, name='productsizeedit'),
    
    path('activateproduct/<int:product_id>/', views.activateproduct, name='activateproduct'),    
    
    path('addproduct/', views.addproduct, name='addproduct'),
    path('addpaper/', views.addpaper, name='addpaper'),
    path('addsubstrate/', views.addsubstrate, name='addsubstrate'),
    path('deleteproduct/<int:product_id>/', views.deleteproduct, name='deleteproduct'),
    path('deletepaperconf/<int:paper_id>/', views.deletepaperconf, name='deletepaperconf'),
]