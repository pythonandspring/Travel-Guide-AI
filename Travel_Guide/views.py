from django.shortcuts import redirect, render 
from django.contrib.auth.hashers import make_password
from Travel_Guide.model import Customer


def index_view(request):
    return render(request, 'index.html')

def insert_data_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = make_password(request.POST.get("password"))  

        Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )

        # return redirect('index.html')  #change

    # return render(request, 'insert_data.html') #change
