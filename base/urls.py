from django.urls import path

from . import views

app_name = 'base'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('createticket', views.createTicket, name='createticket'),
    path('updateticket/<str:pk>', views.updateTicket, name='updateTicket'),
    path('deleteticket/<str:pk>', views.deleteTicket, name='deleteTicket'),
    path('tickets/', views.ticketList, name='tickets'),
    path('addvehicle/', views.addVehicle, name='addvehicle'),
    path('deletevehicle/<str:pk>', views.deleteVehicle, name='deleteVehicle'),
    path('updatevehicle/<str:pk>', views.updateVehicle, name='updateVehicle'),
    path('vehicles', views.vehicles, name='vehicles'),
    path('printticket/<str:pk>', views.printTicket, name='printticket'),
    path('participants/', views.participantsList, name='participants'),
]