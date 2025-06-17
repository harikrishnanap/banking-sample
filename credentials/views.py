from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from bankapp.models import Application, AccountType, District, Branches, Document
from django.http import JsonResponse

from django.http import HttpResponseRedirect
# from .forms import ApplicationForm


# Create your views here.


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpass = request.POST['cpass']
        if password == cpass:
            if User.objects.filter(username=username).exists():
                messages.warning(request, "Username already exists!!")
                return redirect('credentials:register')
            elif User.objects.filter(email=email).exists():
                messages.warning(request, "Email already exists!!")
                return redirect('credentials:register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Successfully registered")
                return render(request, 'login.html')
        else:
            messages.warning(request, "Password does not match!!")
            return redirect('credentials:register')

    return render(request, 'register.html')


def application(request):
    district_collect = District.objects.all()
    branches = Branches.objects.all()
    types = AccountType.objects.all()
    doc = Document.objects.all()

    if request.method == 'POST':
        print("POST data:", request.POST)
        name = request.POST['name']
        dob = request.POST['dob']
        age = request.POST['age']
        email = request.POST['email']
        phone = request.POST['txtEmpPhone']
        district_id = request.POST.get('district')
        district = District.objects.get(pk=district_id)

        # Fetch branches based on the selected district
        branches = Branches.objects.filter(district=district)
        branch_instance = branches.first()

        accType = request.POST.get('types')
        account = AccountType.objects.get(Type_name=accType)
        docType = request.POST.get('document')
        document = Document.objects.get(name=docType)

        # gender = request.POST['gender']
        # materials = request.POST['materials']
        if Application.objects.filter(email=email).exists():
            messages.warning(request, "email already exists!!")
            return redirect('credentials:application')
        elif Application.objects.filter(phone=phone).exists():
            messages.warning(request, "Phone number already exists!!")
            return redirect('credentials:application')
        else:
            application = Application(name=name, dob=dob, age=age, email=email, phone=phone, district=district, branch=branch_instance, account=account, document=document)
            application.save()
            # print(district_drop)
            return render(request, 'applied.html')

    return render(request, 'application.html', {'district': district_collect, 'branch': branches, 'types': types, 'document': doc})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'gotopage.html')
        else:
            messages.warning(request, "Invalid Username or Password")
            return redirect('credentials:login')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')

def get_branches(request, district_id):
    try:
        branches = Branches.objects.filter(district_id=district_id).values('id', 'name')
        return JsonResponse(list(branches), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#
# def formApplication(request):
#     form = ApplicationForm()
#     if request.method == "POST":
#         form = ApplicationForm(request.POST)
#         if form.is_valid():
#             form.save()
#         return render(request, 'demoApplication.html', {"form": form})
