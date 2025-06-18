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

        # Get all form data
        name = request.POST.get('name', '').strip()
        dob = request.POST.get('dob', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('txtEmpPhone', '').strip()
        district_id = request.POST.get('district', '').strip()
        accType = request.POST.get('types', '').strip()
        docType = request.POST.get('document', '').strip()
        age_str = request.POST.get('age', '').strip()

        # Debug print
        print(f"District ID received: '{district_id}' (type: {type(district_id)})")

        # Validation function to render form with error
        def render_form_with_error(error_message):
            messages.error(request, error_message)
            return render(request, 'application.html', {
                'district': district_collect,
                'branch': branches,
                'types': types,
                'document': doc
            })

        # Validate all required fields
        if not name:
            return render_form_with_error("Name is required!")

        if not email:
            return render_form_with_error("Email is required!")

        if not dob:
            return render_form_with_error("Date of birth is required!")

        if not phone:
            return render_form_with_error("Phone number is required!")

        if not district_id or district_id == "":
            return render_form_with_error("District is required!")

        if not accType or accType == "":
            return render_form_with_error("Account type is required!")

        if not docType or docType == "":
            return render_form_with_error("Document type is required!")

        # Get branch selection
        branch_id = request.POST.get('branch', '').strip()
        if not branch_id or branch_id == "":
            return render_form_with_error("Branch is required!")

        # Validate age field
        if not age_str:
            return render_form_with_error("Age is required!")

        try:
            age = int(age_str)
            if age < 18:
                return render_form_with_error("Age must be 18 or above!")
        except ValueError:
            return render_form_with_error("Please enter a valid age!")

        # Validate email format (basic check)
        if '@' not in email or '.' not in email:
            return render_form_with_error("Please enter a valid email address!")

        # Validate phone number length
        if len(phone) < 10:
            return render_form_with_error("Phone number must be at least 10 digits!")

        # Get related objects with error handling
        try:
            district_id = int(district_id)  # Convert to integer first
            district = District.objects.get(pk=district_id)
        except (ValueError, TypeError):
            return render_form_with_error("Invalid district selection!")
        except District.DoesNotExist:
            return render_form_with_error("Selected district does not exist!")

        try:
            account = AccountType.objects.get(Type_name=accType)
        except AccountType.DoesNotExist:
            return render_form_with_error("Selected account type is invalid!")

        try:
            document = Document.objects.get(name=docType)
        except Document.DoesNotExist:
            return render_form_with_error("Selected document type is invalid!")

        # Get branch with validation
        try:
            branch_id = int(branch_id)
            branch_instance = Branches.objects.get(pk=branch_id)
            # Verify that the branch belongs to the selected district
            if branch_instance.district != district:
                return render_form_with_error("Selected branch does not belong to the chosen district!")
        except (ValueError, TypeError):
            return render_form_with_error("Invalid branch selection!")
        except Branches.DoesNotExist:
            return render_form_with_error("Selected branch does not exist!")

        # Remove the old automatic branch selection code
        # branches_filtered = Branches.objects.filter(district=district)
        # if not branches_filtered.exists():
        #     return render_form_with_error("No branches available for the selected district!")
        # branch_instance = branches_filtered.first()

        # Check for duplicate email and phone
        if Application.objects.filter(email=email).exists():
            messages.warning(request, "Email already exists!!")
            return redirect('credentials:application')

        if Application.objects.filter(phone=phone).exists():
            messages.warning(request, "Phone number already exists!!")
            return redirect('credentials:application')

        # Create and save the application
        try:
            application = Application(
                name=name,
                dob=dob,
                age=age,
                email=email,
                phone=phone,
                district=district,
                branch=branch_instance,
                account=account,
                document=document
            )
            application.save()
            messages.success(request, "Application submitted successfully!")
            return render(request, 'applied.html')
        except Exception as e:
            return render_form_with_error(f"Error saving application: {str(e)}")

    return render(request, 'application.html', {
        'district': district_collect,
        'branch': branches,
        'types': types,
        'document': doc
    })
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
