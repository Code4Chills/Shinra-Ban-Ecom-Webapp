from .cart import Cart


#create context proxcessor so our cart can work on all pages
def cart(request):
	#Return the default data from our Cart
	return {'cart': Cart(request)}