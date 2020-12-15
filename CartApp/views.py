from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data.get("phone"))
            user = form.save()
            username = form.cleaned_data.get("username")
            print(form.cleaned_data)
            name = (
                form.cleaned_data.get("first_name")
                + " "
                + form.cleaned_data.get("last_name")
            )
            group = Group.objects.get(name="customer")
            user.groups.add(group)
            Customer.objects.create(user=user, name=name)
            messages.success(request, "Account was created for " + username)
            return redirect("login")

    context = {"form": form}
    return render(request, "CartApp/register.html", context)


@unauthenticated_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "username or password is incorrect.")
            return render(request, "CartApp/login.html")

    context = {}
    return render(request, "CartApp/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    deliverd = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {
        "orders": orders,
        "total_orders": total_orders,
        "deliverd": deliverd,
        "pending": pending,
    }
    return render(request, "CartApp/user.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def account_settings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        print(form.cleaned_data )
        if form.is_valid():
            form.save()
    context = {"form": form}
    return render(request, "CartApp/account_settings.html", context)


@login_required(login_url="login")
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_orders = orders.count()
    total_customers = customers.count()
    deliverd = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()
    context = {
        "orders": orders,
        "customers": customers,
        "total_orders": total_orders,
        "total_customers": total_customers,
        "deliverd": deliverd,
        "pending": pending,
    }
    return render(request, "CartApp/dashboard.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def products(request):
    product = Product.objects.all()
    return render(request, "CartApp/products.html", {"products": product})


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def customer(request, pk_):
    customers = Customer.objects.get(id=pk_)
    orders = customers.order_set.all()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        "customer": customers,
        "orders": orders,
        "total_orders": orders.count(),
        "myFilter": myFilter,
    }

    return render(request, "CartApp/customer.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=("product", "status"), extra=10
    )
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == "POST":
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect("/")
    context = {"formset": formset}
    return render(request, "CartApp/order_form.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {"form": form}
    return render(request, "CartApp/order_form.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect("/")
    context = {"item": order}
    return render(request, "CartApp/delete.html", context)

