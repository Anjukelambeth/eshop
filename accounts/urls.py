
from django.urls import path
from accounts import views

urlpatterns = [
     path('signout/',views.signout,name='signout'),
     path('',views.store, name='store'),
]
