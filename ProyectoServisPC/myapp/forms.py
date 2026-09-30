from django import forms
from .models import Cliente, Opinion

class ClientesFormulario(forms.Form):
    nombre = forms.CharField(max_length=100, label="Nombre")
    apellido = forms.CharField(max_length=100, label="Apellido")
    telefono = forms.CharField(max_length=20, label="Teléfono")
    email = forms.EmailField(label="Correo Electrónico")
    direccion = forms.CharField(max_length=200, label="Dirección")
    
    
class ClientesFilter(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'email']
        
        

class OpinionForm(forms.ModelForm):
    class Meta:
        model = Opinion
        fields = ['estrellas', 'comentario']
        widgets = {
            'comentario': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Escriba su opinión sobre la atención recibida...'
                }
            )
        }