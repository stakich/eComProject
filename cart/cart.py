from decimal import Decimal
from store.models import Product


class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_cart')

        if 'session_cart' not in request.session:
            cart = self.session['session_cart'] = {}

        self.cart = cart


    def add(self, product, qty):

        product_id = str(product.id)
        
        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
            
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': qty}

        self.session.modified = True

        
    def delete(self, product):

        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())
    
    def __iter__(self):
        
        product_ids = [int(pid) for pid in self.cart.keys()]
        products = Product.objects.filter(id__in=product_ids)

        product_map = {p.id: p for p in products}

        # 3. Single loop: pull data, convert price, compute total, attach product
        for pid_str, item in self.cart.items():
            pid   = int(pid_str)
            price = Decimal(item['price'])
            qty   = item['qty']
            yield {
                'product': product_map.get(pid),
                'price':   price,
                'qty':     qty,
                'total':   price * qty,
            }

    def get_total(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
            

    def update(self, product, qty):

        product_id = str(product)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty
        

        self.session.modified = True