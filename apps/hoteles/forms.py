from django import forms
from .models import BusquedaHotel, ReservaHotel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class BusquedaHotelForm(forms.ModelForm):
    """Formulario para búsqueda de hoteles."""
    
    class Meta:
        model = BusquedaHotel
        fields = [
            'destino', 'fecha_entrada', 'fecha_salida',
            'adultos', 'ninos', 'habitaciones',
            'precio_min', 'precio_max', 'categoria_min', 'categoria_max'
        ]
        widgets = {
            'fecha_entrada': forms.DateInput(attrs={'type': 'date'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date'}),
            'precio_min': forms.NumberInput(attrs={'placeholder': 'Mínimo'}),
            'precio_max': forms.NumberInput(attrs={'placeholder': 'Máximo'}),
        }
        labels = {
            'destino': 'Destino (ciudad o país)',
            'fecha_entrada': 'Fecha de entrada',
            'fecha_salida': 'Fecha de salida',
            'adultos': 'Adultos',
            'ninos': 'Niños',
            'habitaciones': 'Habitaciones',
            'precio_min': 'Precio mínimo por noche',
            'precio_max': 'Precio máximo por noche',
            'categoria_min': 'Categoría mínima (estrellas)',
            'categoria_max': 'Categoría máxima (estrellas)',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        fecha_entrada = cleaned_data.get('fecha_entrada')
        fecha_salida = cleaned_data.get('fecha_salida')
        precio_min = cleaned_data.get('precio_min')
        precio_max = cleaned_data.get('precio_max')
        categoria_min = cleaned_data.get('categoria_min')
        categoria_max = cleaned_data.get('categoria_max')
        
        # Validar fechas
        if fecha_entrada and fecha_salida:
            if fecha_entrada >= fecha_salida:
                raise forms.ValidationError("La fecha de entrada debe ser anterior a la fecha de salida.")
            if fecha_entrada < timezone.now().date():
                raise forms.ValidationError("La fecha de entrada no puede ser en el pasado.")
        
        # Validar precios
        if precio_min and precio_max:
            if precio_min > precio_max:
                raise forms.ValidationError("El precio mínimo no puede ser mayor que el precio máximo.")
        
        # Validar categorías
        if categoria_min and categoria_max:
            if categoria_min > categoria_max:
                raise forms.ValidationError("La categoría mínima no puede ser mayor que la categoría máxima.")
        
        return cleaned_data

class ReservaHotelForm(forms.ModelForm):
    """Formulario para crear una reserva de hotel."""
    
    confirmar_email = forms.EmailField(
        label="Confirmar email",
        help_text="Por favor, confirma tu dirección de email"
    )
    
    aceptar_terminos = forms.BooleanField(
        label="Acepto los términos y condiciones",
        required=True,
        error_messages={'required': 'Debes aceptar los términos y condiciones'}
    )
    
    class Meta:
        model = ReservaHotel
        fields = [
            'nombre_huesped', 'email_huesped', 'confirmar_email', 'telefono_huesped',
            'fecha_entrada', 'fecha_salida', 'adultos', 'ninos', 'habitaciones',
            'observaciones', 'aceptar_terminos'
        ]
        widgets = {
            'fecha_entrada': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
            'adultos': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'ninos': forms.NumberInput(attrs={'min': 0, 'max': 10}),
            'habitaciones': forms.NumberInput(attrs={'min': 1, 'max': 10}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Comentarios adicionales...'}),
        }
        labels = {
            'nombre_huesped': 'Nombre completo del huésped principal',
            'email_huesped': 'Email del huésped',
            'telefono_huesped': 'Teléfono de contacto',
            'fecha_entrada': 'Fecha de check-in',
            'fecha_salida': 'Fecha de check-out',
            'adultos': 'Número de adultos',
            'ninos': 'Número de niños',
            'habitaciones': 'Número de habitaciones',
            'observaciones': 'Observaciones especiales',
        }
        help_texts = {
            'telefono_huesped': 'Incluye código de país (ej: +34)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que los campos de fecha sean de solo lectura
        self.fields['fecha_entrada'].widget.attrs['readonly'] = True
        self.fields['fecha_salida'].widget.attrs['readonly'] = True
    
    def clean(self):
        cleaned_data = super().clean()
        email_huesped = cleaned_data.get('email_huesped')
        confirmar_email = cleaned_data.get('confirmar_email')
        fecha_entrada = cleaned_data.get('fecha_entrada')
        fecha_salida = cleaned_data.get('fecha_salida')
        
        # Validar que los emails coincidan
        if email_huesped and confirmar_email and email_huesped != confirmar_email:
            raise forms.ValidationError("Los emails no coinciden. Por favor, verifica.")
        
        # Validar fechas
        if fecha_entrada and fecha_salida:
            if fecha_entrada >= fecha_salida:
                raise forms.ValidationError("La fecha de entrada debe ser anterior a la fecha de salida.")
            if fecha_entrada < timezone.now().date():
                raise forms.ValidationError("La fecha de entrada no puede ser en el pasado.")
            
            # Validar que la estancia sea de al menos 1 noche
            noches = (fecha_salida - fecha_entrada).days
            if noches < 1:
                raise forms.ValidationError("La estancia debe ser de al menos 1 noche.")
        
        return cleaned_data
    
    def clean_telefono_huesped(self):
        telefono = self.cleaned_data.get('telefono_huesped')
        if telefono:
            # Validación básica de teléfono (puedes mejorar esto)
            if len(telefono) < 9:
                raise forms.ValidationError("Por favor, introduce un número de teléfono válido.")
        return telefono
