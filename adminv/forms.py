from django import forms
from .models import Clientes, Obras, MaterialesF, Materiales
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class FiltroForm(forms.Form):
    opciones = (
        ('todos', 'Todos'),
        ('activos', 'Activos'),
        ('no_activos', 'No Activos'),
    )
    filtro = forms.ChoiceField(choices=opciones)


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['nombre', 'apellido', 'correo',
                  'tel1', 'tel2', 'notas', 'activo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['created_at'] = forms.DateTimeField(
                disabled=True, initial=instance.created_at)


class ObrasForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(queryset=Clientes.objects.filter(activo=True
                                                                      ), widget=forms.Select(attrs={'class': 'form-control'}))
    dir = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    tel = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    activo = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}))

    class Meta:
        model = Obras
        fields = ['cliente', 'dir', 'tel', 'activo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['created_at'] = forms.DateTimeField(
                disabled=True, initial=instance.created_at)


class MaterialesfForm(forms.ModelForm):
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    descrip = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    activo = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = MaterialesF
        fields = ['nombre', 'descrip', 'activo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['created_at'] = forms.DateTimeField(
                disabled=True, initial=instance.created_at)


class MaterialesForm(forms.ModelForm):
    familia = forms.ModelChoiceField(queryset=MaterialesF.objects.filter(
        activo=True), widget=forms.Select(attrs={'class': 'form-control'}))
    nombre = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    descrip = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    activo = forms.BooleanField(widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Materiales
        fields = ['familia', 'nombre', 'descrip', 'activo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['created_at'] = forms.DateTimeField(
                disabled=True, initial=instance.created_at)


class UsuarioNuevoForm(UserCreationForm):
    username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    first_name = forms.CharField(
        label="Nombres", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        label="Apellidos", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label="Contraseña", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    is_superuser = forms.BooleanField(label="Es administrador", widget=forms.CheckboxInput(
        attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', 'is_superuser']


class UsuarioEditarForm(forms.ModelForm):
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label="Nombres",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label="Apellidos",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text=False,
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text=False,
    )
    is_active = forms.BooleanField(
        label="Usuario Activo",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )
    is_superuser = forms.BooleanField(
        label="Es administrador",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'is_superuser', 'is_active']
