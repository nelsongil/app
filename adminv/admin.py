from django.contrib import admin
from .models import Clientes, Obras


class ClientesAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)


class ObrasAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)

# Register your models here.
admin.site.register(Clientes, ClientesAdmin)
admin.site.register(Obras, ObrasAdmin)