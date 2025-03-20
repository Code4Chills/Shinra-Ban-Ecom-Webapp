from Estore.models import Product, Profile
import decimal


class Cart():
	def __init__(self, request):
		self.session=request.session

		#Get request
		self.request=request

		#Get the current session key if it exists
		cart= self.session.get('session_key')

		#If the user is new, no session key!create one
		if 'session_key' not in self.session:
			cart=self.session['session_key']={}


		#Make sure cart is available on all pages of site
		
		self.cart=cart
#Context processor: template put in django->django looks in acertain place to find it

	def add(self, product, quantity):
		product_id=str(product.id)
		product_qty=str(quantity)
		
		#Logic
		if product_id in self.cart:
			pass

		else:
			#self.cart[product_id]={'price': str(product.price)}
			self.cart[product_id]=int(product_qty)

		self.session.modified=True 


		#Deal with Logged in User 
		if self.request.user.is_authenticated:
			#Get the current user profile
			current_user=Profile.objects.filter(user__id=self.request.user.id)

			#"{'3': 1, '2': 3}" to {"3":1, "2":5}
			carty=str(self.cart)
			carty=carty.replace("\'", "\"")

			#save carty to Profile model
			current_user.update(old_cart=str(carty))

	def db_add(self, product, quantity):
		product_id=str(product)
		product_qty=str(quantity)

		#Logic
		if product_id in self.cart:
			pass

		else:
			#self.cart[product_id]={'price': str(product.price)}
			self.cart[product_id]=int(product_qty)

		self.session.modified=True 


		#Deal with Logged in User 
		if self.request.user.is_authenticated:
			#Get the current user profile
			current_user=Profile.objects.filter(user__id=self.request.user.id)

			#{'3': 1, '2': 3} to {"3":1, "2":5}
			carty=str(self.cart)
			carty=carty.replace("\'", "\"")

			#save carty to Profile model
			current_user.update(old_cart=str(carty))





	def __len__(self):
		return len(self.cart)


	def get_products(self):
		#Get ids from cart
		product_ids=self.cart.keys()

		#use ids to look up products in database
		products=Product.objects.filter(id__in=product_ids)

		#return lookedup products
		return products

	def get_quants(self):
		quantities=self.cart
		return quantities 


	def update(self, product,quantity):
		product_id=str(product)
		product_qty=int(quantity)


		#To update: get cart
		ourcart=self.cart
		#update Dictionary/cart
		ourcart[product_id]=product_qty


		self.session.modified=True

		#Deal with Logged in User 
		if self.request.user.is_authenticated:
			#Get the current user profile
			current_user=Profile.objects.filter(user__id=self.request.user.id)

			#{'3': 1, '2': 3} to {"3":1, "2":5}
			carty=str(self.cart)
			carty=carty.replace("\'", "\"")

			#save carty to Profile model
			current_user.update(old_cart=str(carty))



		cart_update=self.cart
		return cart_update


	def delete(self, product):
		product_id=str(product)

		#Delete from dictionary/cart
		if product_id in self.cart:
			del self.cart[product_id]

		self.session.modified=True

		#Deal with Logged in User 
		if self.request.user.is_authenticated:
			#Get the current user profile
			current_user=Profile.objects.filter(user__id=self.request.user.id)

			#{'3': 1, '2': 3} to {"3":1, "2":5}
			carty=str(self.cart)
			carty=carty.replace("\'", "\"")

			#save carty to Profile model
			current_user.update(old_cart=str(carty))


	def cart_total(self):
		#Get product IDs
		product_ids=self.cart.keys()

		#lookup those keys in products database model
		products=Product.objects.filter(id__in=product_ids)

		#get quantities
		quantities=self.cart

		#start countring at zero
		total= 0
		for key, value in quantities.items():

			key=int(key)
			for product in products:
				if product.id==key:
					if product.is_sale:

						total=total +(float(product.sale_price) * int(value))
					else:
						total=total +(float(product.price) * int(value))


		return total
