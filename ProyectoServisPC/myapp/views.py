from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Tecnico, Equipo, Reparacion, Opinion
from .forms import ClientesFormulario, ClientesFilter, OpinionForm
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Avg, Count

# Create your views here.
def index(request):
    context = {"mensaje":"Ofrecemos servicios de reparación de computadoras, mantenimiento y soporte técnico."}
    return render(request,"myapp/index.html",context)

def clientes(request):
    query = request.GET.get('q')  # Captura lo que se escribe en el buscador
    if query:
        clientes = Cliente.objects.filter(
            models.Q(nombre__icontains=query) |
            models.Q(apellido__icontains=query) |
            models.Q(email__icontains=query)
        )
    else:
        clientes = Cliente.objects.all()


    return render(request, 'myapp/clientes.html', {
        'clientes': clientes,
        'query': query,
    })

def equipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'myapp/equipos.html', {'equipos': equipos})

def tecnicos(request):
    tecnicos = Tecnico.objects.all()
    return render(request, 'myapp/tecnicos.html', {'tecnicos': tecnicos})

def reparaciones(request):
    reparaciones = Reparacion.objects.all()
    return render(request, 'myapp/reparacion.html', {'reparaciones': reparaciones})

@login_required
def agregar_cliente(request):
    if request.method == 'POST':
        form = ClientesFormulario(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            telefono = form.cleaned_data['telefono']
            email = form.cleaned_data['email']
            direccion = form.cleaned_data['direccion']
            cliente = Cliente(nombre=nombre, apellido=apellido, telefono=telefono, email=email, direccion=direccion)
            cliente.save()
            return redirect('myapp:clientes')
    else:
        form = ClientesFormulario()
    return render(request, 'myapp/agregar_cliente.html', {'form': form})

@login_required
def editar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    
    if request.method == 'POST':
        form = ClientesFilter(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('myapp:clientes')
    else:
        form = ClientesFilter(instance=cliente)
    
    return render(request, 'myapp/editar_cliente.html', {'form': form, 'cliente': cliente})

@login_required
def eliminar_cliente(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        cliente.delete()
        return redirect('myapp:clientes')

    return render(request, 'myapp/clientes.html', {'cliente': cliente})




def detalle_tecnico(request, tecnico_id): 
    tecnico = get_object_or_404( 
        Tecnico, 
        id=tecnico_id )
    resultado = Opinion.objects.filter(
        reparacion__tecnico=tecnico 
    ).aggregate( 
        promedio=Avg('estrellas'),
        cantidad=Count('id') 
    ) 
    promedio = resultado['promedio'] 
    cantidad = resultado['cantidad'] 
    return render( 
        request, 
        'myapp/detalle_tecnico.html', 
        { 
            'tecnico': tecnico, 
            'promedio': promedio, 
            'cantidad': cantidad, 
        } )
    
    
    
def crear_opinion(request, reparacion_id):
    reparacion = get_object_or_404(
        Reparacion,
        id=reparacion_id
    )
    # Verificar que la reparación esté entregada
    if reparacion.estado != 'ENTREGADO':
        return redirect('myapp:reparaciones')
    # Verificar si ya tiene una opinión
    if hasattr(reparacion, 'opinion'):
        return redirect('myapp:detalle_reparacion', reparacion_id=reparacion.id)
    if request.method == 'POST':
        form = OpinionForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.reparacion = reparacion
            opinion.save()
            return redirect(
                'myapp:detalle_reparacion',
                reparacion_id=reparacion.id
            )
    else:
        form = OpinionForm()
    return render(
        request,
        'myapp/crear_opinion.html',
        {
            'form': form,
            'reparacion': reparacion,
        }
    )
    
    

def detalle_reparacion(request, reparacion_id):

    reparacion = get_object_or_404(
        Reparacion,
        id=reparacion_id
    )

    return render(
        request,
        'myapp/detalle_reparacion.html',
        {
            'reparacion': reparacion,
        }
    )