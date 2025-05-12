
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
