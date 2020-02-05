from django.shortcuts import render
from .models import InterestForm

# Create your views here.


def home(request):

    return render(request, 'index.html')


def interest(request):

    if request.method == "POST":
        name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        phno = request.POST.get('phno', '')
        city = request.POST.get('city', "")
        interest_list = request.POST.getlist('checkbox[]', '')
        interest = ""
        for i in range(len(interest_list)):
            interest += interest_list[i] + " "
        print(interest)
        inst = InterestForm(name=name, phone_number=phno, email=email, city=city, interest=interest)
        inst.save()
        print(inst)

        return render(request, 'adminusers/logout.html')

    return render(request, 'form1.html')

    # address = request.POST.get('address', "")
    # state = request.POST.get('state', "")
    # zipcode = request.POST.get('zipcode', "")

    # order = Order(items=items, name=name, email=email, address=address, city=city, state=state, zipcode=zipcode, total=total)
    # order.save()
