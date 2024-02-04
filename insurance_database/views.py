from django.shortcuts import render
from django.views import generic

from .models import InsuredPerson, User
from .forms import InsuredPersonForm, UserForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class InsuredPersonIndex(generic.ListView):

    template_name = "insurance_database/insured_person_index.html"
    context_object_name = "insured_persons"

    def get_queryset(self):
        return InsuredPerson.objects.all().order_by("last_name")

class CurrentInsuredPersonView(generic.DetailView):

    model = InsuredPerson
    template_name = "insurance_database/insured_person_detail.html"
    
    def get(self, request, pk):
        try:
            insured_person = self.get_object()
        except:
            return redirect("insured_person_index")
        return render(request, self.template_name, {"insured_person": insured_person})
        
    def post(self, request, pk):
        if request.user.is_authenticated:
            if "edit" in request.POST:
                return redirect("edit_insured_person", pk=self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "You don't have permission to delete an insured person.")
                    return redirect(reverse("insured_person_index"))
                else:
                    self.get_object().delete()
        return redirect(reverse("insured_person_index"))

class CreateInsuredPerson(LoginRequiredMixin, generic.edit.CreateView):

    form_class = InsuredPersonForm
    template_name = "insurance_database/create_insured_person.html"

    def get(self, request):
        if not request.user.is_admin:
            messages.info(request, "You don't have permission to add an insured person.")
            return redirect(reverse("insured_person_index"))
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if not request.user.is_admin:
            messages.info(request, "You don't have permission to add an insured person.")
            return redirect(reverse("insured_person_index"))			
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("insured_person_index")
        return render(request, self.template_name, {"form": form})

class EditInsuredPerson(LoginRequiredMixin, generic.edit.CreateView):
    form_class = InsuredPersonForm
    template_name = "insurance_database/create_insured_person.html"
    
    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "You don't have permission to edit an insured person.")
            return redirect(reverse("insured_person_index"))
        try:
            insured_person = InsuredPerson.objects.get(pk=pk)
        except:
            messages.error(request, "This insured person does not exist!")
            return redirect("insured_person_index")
        form = self.form_class(instance=insured_person)
        return render(request, self.template_name, {"form": form})

    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "You don't have permission to edit an insured person.")
            return redirect(reverse("insured_person_index"))
        form = self.form_class(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            age = form.cleaned_data["age"]
            insurance = form.cleaned_data["insurance"]
            detail_insurance = form.cleaned_data["detail_insurance"]
            try:
                insured_person = InsuredPerson.objects.get(pk=pk)
            except:
                messages.error(request, "This insured person does not exist!")
                return redirect(reverse("insured_person_index"))
            insured_person.first_name = first_name
            insured_person.last_name = last_name
            insured_person.age = age
            insured_person.insurance = insurance
            insured_person.detail_insurance.set(detail_insurance)
            insured_person.save()
        return redirect("insured_person_detail", pk=insured_person.id)

class UserViewRegister(generic.edit.CreateView):
    form_class = UserForm
    model = User
    template_name = "insurance_database/user_form.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in and cannot register.")
            return redirect(reverse("insured_person_index"))            
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in and cannot register.")
            return redirect(reverse("insured_person_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect("insured_person_index")
            
        return render(request, self.template_name, {"form": form})

class UserViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = "insurance_database/user_form.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in and cannot log in again.")
            return redirect(reverse("insured_person_index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in and cannot log in again.")
            return redirect(reverse("insured_person_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("insured_person_index")
            else:
                messages.error(request, "This account does not exist.")
        return render(request, self.template_name, {"form": form})

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, "You cannot log out if you are not logged in.")
    return redirect(reverse("login"))
