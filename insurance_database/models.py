from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Insurance(models.Model):
    insurance_name = models.CharField(max_length=80, verbose_name="Insurance")

    def __str__(self):
        return "{0}".format(self.insurance_name)

    class Meta:
        verbose_name="Insurance"
        verbose_name_plural="Insurances"
		
class InsuranceDetail(models.Model):
    detail_title = models.CharField(max_length = 30, verbose_name="Insurance Detail")

    def __str__(self):
        return self.detail_title

    class Meta:
        verbose_name = "Insurance Detail"
        verbose_name_plural = "Insurance Details"		

class InsuredPerson(models.Model):
    first_name = models.CharField(max_length=200, verbose_name="First Name")
    last_name = models.CharField(max_length=180, verbose_name="Last Name")
    age = models.CharField(max_length=180, default='', verbose_name="Age")
    address = models.CharField(max_length=180, default='', verbose_name="Address")
    insurance = models.ForeignKey(Insurance, on_delete=models.SET_NULL, null=True, verbose_name="Insurance Type")
    detail_insurance = models.ManyToManyField(InsuranceDetail)
	
    def __str__(self):
        detail_insurance = ", ".join(i.detail_title for i in self.detail_insurance.all())
        return "First Name: {0} | Last Name: {1} | Age: {2} | Address: {3} | Insurance: {4} | Detail Insurance: {5}".format(
            self.first_name, self.last_name, self.age, self.address, self.insurance.insurance_name, detail_insurance
        )

    class Meta:
        verbose_name = "Insured Person"
        verbose_name_plural = "Insured Persons"
	
class UserManager(BaseUserManager):
    # Create a user
    def create_user(self, email, password):
        if email and password:
            user = self.model(email=self.normalize_email(email))
            user.set_password(password)
            user.save()
        return user

    # Create an admin
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()
        return user
		
class User(AbstractBaseUser):
    email = models.EmailField(max_length=300, unique=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return "Email: {}".format(self.email)
    
    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
