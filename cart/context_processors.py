#Context processors	can	reside anywhere	in your code, but creating	them here will keep	your code well organized.
#A	context	processor	is	a	function	that	receives	the	request	object	as	a
#parameter	and	returns	a	dictionary	of	objects	that	will	be	available
#to	all	the	templates	rendered	using	RequestContext.

from .cart import Cart

def cart(request):
    return{'cart': Cart(request)}
    