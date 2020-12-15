from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_funk):
	def wrapper_funk(request,*args,**kwargs):
		if request.user.is_authenticated:
			return redirect("home")
		else:
        	
        
			return view_funk(request,*args,**kwargs)
	return wrapper_funk



def allowed_users(allowed_roles=[]):
	def decorator(view_funk):
		def wrapper_funk(request,*args,**kwargs):
			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			if group in allowed_roles:
				return view_funk(request,*args,**kwargs)
			else:
				return HttpResponse("You are not authorized.")
		return wrapper_funk
	return decorator


def admin_only(view_funk):
	def wrapper_func(request,*args,**kwargs):
		group = None
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name

		if group == "customer":
			return redirect("userPage")

		if group == "admin":
			return view_funk(request,*args,**kwargs)
	return wrapper_func