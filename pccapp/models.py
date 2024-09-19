from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class Product(models.Model):
    
    UOM_CHOICES = [
        ('NO', 'No\'s'),
        ('ROLL', 'Roll'),
        ('PCS', 'Pcs'),
        ('SQM', 'SqM'),
    ]
    
    name = models.CharField(max_length=50)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    uom = models.CharField(max_length=10, choices=UOM_CHOICES) 
    status = models.IntegerField(default=0)
    min_quantity = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class PaperType(models.Model):
    name = models.CharField(max_length=50)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    width = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    cost_adjustment = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.width} x {self.height} ({self.product.name})"

class PaperThickness(models.Model):
    gsm = models.IntegerField()
    cost_adjustment = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.gsm} GSM"

class PaperSize(models.Model):
    name = models.CharField(max_length=5)
    width = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=7, decimal_places=2)
    cost_adjustment = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.width} x {self.height} ({self.name})"

class PaperConfiguration(models.Model):
    paper_type = models.ForeignKey(PaperType, on_delete=models.CASCADE)
    paper_size = models.ForeignKey(PaperSize, on_delete=models.CASCADE)
    paper_thickness = models.ForeignKey(PaperThickness, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('paper_type', 'paper_size', 'paper_thickness')

    def __str__(self):
        return f"{self.paper_type}, {self.paper_size}, {self.paper_thickness}"

class Substrate(models.Model):
    name = models.CharField(max_length=50)
    base_cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class SubstrateSize(models.Model):
    width = models.DecimalField(max_digits=5, decimal_places=2)
    height = models.DecimalField(max_digits=7, decimal_places=2)
    cost_adjustment = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.width} x {self.height}"

class SubstrateThickness(models.Model):
    thickness_value = models.DecimalField(max_digits=5, decimal_places=2)
    cost_adjustment = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.thickness_value}mm"

class SubstrateConfiguration(models.Model):
    substrate = models.ForeignKey(Substrate, on_delete=models.CASCADE)
    substrate_size = models.ForeignKey(SubstrateSize, on_delete=models.CASCADE)
    substrate_thickness = models.ForeignKey(SubstrateThickness, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('substrate', 'substrate_size', 'substrate_thickness')

    def __str__(self):
        return f"Substrate Config ({self.substrate}, {self.substrate_size}, {self.substrate_thickness})"
    
class CalculationRecord(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    number_of_products = models.PositiveIntegerField()
    grand_total = models.DecimalField(max_digits=10, decimal_places=2)
    time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')