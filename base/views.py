from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, Bus
from .forms import TicketForm, VehicleForm
from datetime import datetime, timedelta
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
import qrcode

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    tickets = Ticket.objects.all().count()
    buses = Bus.objects.all().count()
    context = {'tickets': tickets, 'buses': buses}
    return render(request, 'base/dashboard.html', context);

@login_required(login_url='login')
def createTicket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            fcd = form.cleaned_data
            ticket = Ticket(
                first_name = fcd['first_name'],
                last_name = fcd['last_name'],
                vehicle = Bus.objects.get(id=fcd['vehicle']),
                issued_by = request.user,
                expiry_date = datetime.now() + timedelta(days=30)
            )
            ticket.save()
            return redirect('/')
    form = TicketForm()
    context = {'form': form, 'heading': 'create ticket'}
    return render(request, 'base/form.html', {'form': form})

@login_required(login_url='login')
def addVehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
    
    form = VehicleForm()
    context = {'form': form, 'heading': 'Add vehicle information'}
    return render(request, 'base/form.html', context)

@login_required(login_url='login')
def deleteVehicle(request, pk):
    vehicle = Bus.objects.get(id=pk)
    vehicle.delete()
    return redirect('base:dashboard')

@login_required(login_url='login')
def updateVehicle(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()

    form = VehicleForm(instance=bus)
    context = {'form': form, 'heading': 'update vehicle information'}
    return render(request, 'base/form.html', context)

@login_required(login_url='login')
def vehicles(request):
    vehicles = Bus.objects.all()
    context = {'vehicles': vehicles}
    return render(request, 'base/vehicleList.html', context)       
        

@login_required(login_url='login')
def ticketList(request):
    tickets = Ticket.objects.all()
    context = {'tickets': tickets}
    return render(request, 'base/ticketlist.html', context)

@login_required(login_url='login')
def updateTicket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST) 
        if form.is_valid():
            fcd = form.cleaned_data
            ticket.first_name = fcd['first_name']
            ticket.last_name = fcd['last_name']
            ticket.vehicle = Bus.objects.get(id=fcd['vehicle'])
            ticket.save()
            return redirect('dashboard')

    form = TicketForm(initial={'first_name': ticket.first_name, 'last_name': ticket.last_name, 'vehicle': ticket.vehicle})
    context = {'form': form, 'heading': 'update ticket information'}
    return render(request, 'base/form.html', context)    

@login_required(login_url='login')
def deleteTicket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    ticket.delete()
    return redirect('dashboard')

@login_required(login_url='login')
def printTicket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)

    p.drawString(220, 720, 'Bayero University shuttle ticket')

    p.rect(20, 500, 550, 200, stroke=1, fill=0)

    code = qrcode.make(f'{ticket.first_name}+{ticket.id}+{ticket.vehicle.number}')

    p.rect(140, 545, 240, 120, stroke=1, fill=0)

    p.drawImage('logo.png', 40, 540, width=100, height=120, mask=[0,1,0,1,0,1])

    code.save('qrcode.png')

    p.drawString(150, 630, f'First Name: {ticket.first_name}')

    p.drawString(150, 610, f'Last Name: {ticket.last_name}')

    p.drawString(150, 590, f'Vehicle Model: {ticket.vehicle.model_name}')

    p.drawString(150, 570, f'Vehicle Number: {ticket.vehicle.number}')

    p.drawImage('qrcode.png', 390, 515, width=170, height=170, mask=None)

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='ticket.pdf')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist') 

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('base:dashboard')
        else: 
            messages.error(request, 'username or password is not correct')   
  
    context = {}
    return render(request, 'base/login.html', context)
    

def logoutPage(request):
    logout(request)
    return redirect('base:login')