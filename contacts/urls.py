from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),

    path('', views.user_login, name='login'),

    path('contact-list/', views.listing, name='listing'),

    path('add/', views.contact_list, name='contact_list'),

    path('logout/', views.user_logout, name='logout'),

    path('delete/<int:id>/', views.delete_contact, name='delete_contact'),

    path('edit/<int:id>/', views.edit_contact, name='edit_contact'),

    path('detail/<int:id>/', views.contact_detail, name='contact_detail'),

    path('logout/', views.user_logout, name='logout'),
]
