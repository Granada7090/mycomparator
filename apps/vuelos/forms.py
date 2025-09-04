from django import forms
from .models import BusquedaVuelo, Aeropuerto

class BusquedaVueloForm(forms.ModelForm):
    TIPO_VUELO_CHOICES = [
        ('ida', 'Solo ida'),
        ('ida_vuelta', 'Ida y vuelta'),
    ]
    
    CLASE_CHOICES = [
        ('economy', 'Económica'),
        ('premium', 'Premium Economy'),
        ('business', 'Business'),
        ('first', 'First Class'),
    ]

    tipo_vuelo = forms.ChoiceField(
        choices=TIPO_VUELO_CHOICES,
        initial='ida_vuelta',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        label='Tipo de vuelo'
    )
    
    origen = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ciudad o aeropuerto de origen',
            'autocomplete': 'off'
        }),
        label='Origen'
    )
    
    destino = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ciudad o aeropuerto de destino',
            'autocomplete': 'off'
        }),
        label='Destino'
    )
    
    fecha_salida = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': '2025-09-03'
        }),
        label='Fecha de ida'
    )
    
    fecha_regreso = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': '2025-09-03'
        }),
        label='Fecha de vuelta'
    )
    
    pasajeros_adultos = forms.IntegerField(
        min_value=1,
        max_value=9,
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '9'
        }),
        label='Adultos'
    )
    
    pasajeros_ninos = forms.IntegerField(
        min_value=0,
        max_value=9,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '9'
        }),
        label='Niños'
    )
    
    pasajeros_bebes = forms.IntegerField(
        min_value=0,
        max_value=9,
        initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'max': '9'
        }),
        label='Bebés'
    )
    
    clase = forms.ChoiceField(
        choices=CLASE_CHOICES,
        initial='economy',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Clase'
    )

    class Meta:
        model = BusquedaVuelo
        fields = ['origen', 'destino', 'fecha_salida', 'fecha_regreso', 
                 'pasajeros_adultos', 'pasajeros_ninos', 'pasajeros_bebes', 'clase']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar opciones de aeropuertos para autocompletar
        aeropuertos = Aeropuerto.objects.all()
        opciones = [(ap.codigo_iata, f"{ap.ciudad} ({ap.codigo_iata})") for ap in aeropuertos]
        
        # Agregar datos para autocompletar (puedes usar JavaScript para esto)
        self.fields['origen'].widget.attrs.update({'list': 'aeropuertos-lista'})
        self.fields['destino'].widget.attrs.update({'list': 'aeropuertos-lista'})

    def clean(self):
        cleaned_data = super().clean()
        tipo_vuelo = cleaned_data.get('tipo_vuelo')
        fecha_regreso = cleaned_data.get('fecha_regreso')
        
        if tipo_vuelo == 'ida_vuelta' and not fecha_regreso:
            raise forms.ValidationError("La fecha de vuelta es obligatoria para viajes de ida y vuelta.")
        
        if fecha_regreso and cleaned_data.get('fecha_salida'):
            if fecha_regreso < cleaned_data['fecha_salida']:
                raise forms.ValidationError("La fecha de vuelta no puede ser anterior a la fecha de ida.")
        
        return cleaned_data
