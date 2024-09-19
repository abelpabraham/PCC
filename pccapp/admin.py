from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Product)
admin.site.register(PaperType)
admin.site.register(ProductSize)
admin.site.register(PaperSize)
admin.site.register(PaperThickness)
admin.site.register(PaperConfiguration)
admin.site.register(Substrate)
admin.site.register(SubstrateSize)
admin.site.register(SubstrateThickness)
admin.site.register(SubstrateConfiguration)