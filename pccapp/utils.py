from django.shortcuts import get_object_or_404
from . models import *
from decimal import Decimal
import math

def calculate_cost(base_printing_price, size_cost_adjustment, quantity, substrate_cost=None, paper_cost=None, substrate_quantity=None, paper_quantity=None):
    
    printing_cost = base_printing_price * size_cost_adjustment * quantity

    if substrate_cost is not None and substrate_quantity is not None:
        material_cost = substrate_cost  * Decimal(substrate_quantity) 
    else:
        material_cost = paper_cost* Decimal(paper_quantity)

    subtotal = printing_cost + material_cost

    cartridge_cost = subtotal * Decimal('0.10')
    overhead_cost = subtotal * Decimal('0.30')
    grand_total = subtotal + cartridge_cost + overhead_cost

    return {
        'printing_cost': printing_cost,
        'material_cost': material_cost,
        'subtotal': subtotal,
        'cartridge_cost': cartridge_cost,
        'overhead_cost': overhead_cost,
        'grand_total': grand_total
    }

def validate_calculator_form(data):
    errors = []

    selected_product_id = data.get('product')
    selected_size_id = data.get('product_size')
    quantity = data.get('quantity')
    paper_size_id = data.get('paper_size_option')
    substrate_id = data.get('substrate')
    substrate_size_id = data.get('substrate_size')
    substrate_quantity = data.get('substrate_quantity')
    paper_quantity = data.get('paper_quantity')

    if not selected_product_id or not selected_size_id or not quantity:
        errors.append("Please select a product, product size, and provide a quantity.")

    if (paper_size_id and substrate_id) or (not paper_size_id and not substrate_id):
        errors.append("Please select either paper size or substrate (but not both).")

    if substrate_id and not substrate_quantity:
        errors.append("Please provide a quantity for the selected substrate.")

    if paper_size_id and not paper_quantity:
        errors.append("Please provide a quantity for the selected paper size.")

    return errors

def get_selected_objects(selected_product_id, selected_size_id, paper_size_id, substrate_id, substrate_size_id):
    selected_product = get_object_or_404(Product, id=selected_product_id)
    selected_size = get_object_or_404(ProductSize, id=selected_size_id)

    selected_paper_size = get_object_or_404(PaperSize, id=paper_size_id) if paper_size_id else None
    selected_substrate = get_object_or_404(Substrate, id=substrate_id) if substrate_id else None
    selected_substrate_size = get_object_or_404(SubstrateSize, id=substrate_size_id) if substrate_size_id else None

    return selected_product, selected_size, selected_paper_size, selected_substrate, selected_substrate_size

def calculate_cost_details(selected_product, selected_size, quantity, paper_size, substrate, substrate_size, substrate_quantity, paper_quantity):
    paper_cost, substrate_cost = None, None

    if paper_size and paper_quantity:
        paper_cost = Decimal(paper_size.cost_adjustment)

    if substrate and substrate_size and substrate_quantity:
        substrate_cost = Decimal(substrate.base_cost_per_unit)

    base_printing_price = Decimal(selected_product.cost_per_unit)
    size_cost_adjustment = Decimal(selected_size.cost_adjustment)

    cost_details = calculate_cost(
        base_printing_price,
        size_cost_adjustment,
        quantity,
        substrate_cost=substrate_cost,
        paper_cost=paper_cost,
        substrate_quantity=substrate_quantity,
        paper_quantity=paper_quantity
    )

    return cost_details

from decimal import Decimal

def calculate_products_per_sheet(product_size, paper_size):
    product_width_in_inches = float(product_size.width) / 25.4
    product_height_in_inches = float(product_size.height) / 25.4
    paper_width_in_inches = float(paper_size.width) / 25.4
    paper_height_in_inches = float(paper_size.height) / 25.4

    fit_width = paper_width_in_inches // product_width_in_inches
    fit_height = paper_height_in_inches // product_height_in_inches

    total_products = fit_width * fit_height
    return int(total_products)  
