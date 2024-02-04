from django.urls import path, include
from . import views
from . import url_handlers

urlpatterns = [    
    path("insured_person_index/", views.InsuredPersonIndex.as_view(), name="insured_person_index"),
    path("<int:pk>/insured_person_detail/", views.CurrentInsuredPersonView.as_view(), name="insured_person_detail"),
    path("create_insured_person/", views.CreateInsuredPerson.as_view(), name="create_insured_person"),    
    path("<int:pk>/edit/", views.EditInsuredPerson.as_view(), name="edit_insured_person"),
    path("register/", views.UserViewRegister.as_view(), name="registration"),
    path("login/", views.UserViewLogin.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("", url_handlers.index_handler),
]

