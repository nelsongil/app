from django.contrib import admin
from django.urls import path
from adminv import views

urlpatterns = [
    #Home
    path('admin/', admin.site.urls),
    path('', views.home, name='signup'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    #Clientes
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/crear/', views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:cliente_id>/', views.cliente_detalle, name='cliente_detalle'),
    path('clientes/<int:cliente_id>/eliminar', views.cliente_eliminar, name='cliente_eliminar'), 
    #Obras
    path('obras/', views.obras, name='obras'),
    path('obras/crear/', views.obra_crear, name='obra_crear'),
    path('obras/<int:obra_id>/', views.obra_detalle, name='obra_detalle'),
    path('obras/<int:obra_id>/eliminar', views.obra_eliminar, name='obra_eliminar'),
    #Materiales Familia
    path('materialesf/', views.materialesf, name='materialesf'),
    path('materialesf/', views.materialesf, name='materialf'),
    path('materialesf/crear/', views.materialf_crear, name='materialf_crear'),
    path('materialesf/<int:materialf_id>/', views.materialf_detalle, name='materialf_detalle'),
    path('materialesf/<int:materialf_id>/eliminar', views.materialf_eliminar, name='materialf_eliminar'),
    #Materiales 
    path('materiales/', views.materiales, name='materiales'),
    path('materiales/crear/', views.material_crear, name='material_crear'),
    path('materiales/<int:material_id>/', views.material_detalle, name='material_detalle'),
    path('materiales/<int:material_id>/eliminar', views.material_eliminar, name='material_eliminar'),
    #Usuarios
    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/crear/', views.usuario_crear, name='usuario_crear'),
    path('usuarios/<int:usuario_id>/', views.usuario_editar, name='usuario_editar'),
    path('usuarios/<int:usuario_id>/eliminar', views.usuario_eliminar, name='usuario_eliminar'),
    path('logout/', views.signout, name='logout'), 
    
    #home2
    path('home2/', views.home2, name='home2'),
    path('home2/marcar_tarjeta/', views.marcar_tarjeta, name='marcar_tarjeta'),
    path('home2/horas_informe/', views.horas_informe, name='horas_informe'),
    path('home2/horas_informe_semanal/', views.horas_informe_semanal, name='horas_informe_semanal'),

    
    path('login/', views.login, name='login'),
    path('signin/', views.signin, name='signin'),
    
    path('pruebas/', views.pruebas, name='pruebas'),
]
