from decimal import Decimal
from products.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('aleen_cart')
        if not cart:
            cart = self.session['aleen_cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1):
        product_id = str(product.id)
        current_qty = self.cart.get(product_id, {}).get('quantity', 0)
        new_qty = min(current_qty + quantity, product.stock_qty)

        if new_qty > 0:
            self.cart[product_id] = {'quantity': new_qty}
            self.save()

    def update(self, product, quantity):
        product_id = str(product.id)
        if quantity <= 0:
            self.remove(product_id)
        else:
            self.cart[product_id] = {'quantity': min(quantity, product.stock_qty)}
            self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session['aleen_cart'] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def get_items(self):
        product_ids = [int(pid) for pid in self.cart.keys()]
        products = Product.objects.filter(id__in=product_ids, is_available=True)
        product_map = {str(p.id): p for p in products}

        items = []
        for pid, data in list(self.cart.items()):
            product = product_map.get(pid)
            if not product or not product.is_in_stock:
                continue
            qty = min(data['quantity'], product.stock_qty)
            subtotal = product.current_price * qty
            items.append({
                'product': product,
                'id': product.id,
                'name': product.name,
                'slug': product.slug,
                'image': product.image.url if product.image else '',
                'price': product.current_price,
                'quantity': qty,
                'stock_qty': product.stock_qty,
                'subtotal': subtotal,
            })
        return items

    def get_total_price(self):
        return sum((item['subtotal'] for item in self.get_items()), Decimal('0.00'))

    def get_total_count(self):
        return sum(item['quantity'] for item in self.get_items())

    def to_json(self):
        items = self.get_items()
        return {
            'items': [
                {
                    'id': item['id'],
                    'name': item['name'],
                    'slug': item['slug'],
                    'image': item['image'],
                    'price': float(item['price']),
                    'quantity': item['quantity'],
                    'stock_qty': item['stock_qty'],
                    'subtotal': float(item['subtotal']),
                }
                for item in items
            ],
            'total_count': sum(item['quantity'] for item in items),
            'subtotal': float(sum((item['subtotal'] for item in items), Decimal('0.00'))),
        }