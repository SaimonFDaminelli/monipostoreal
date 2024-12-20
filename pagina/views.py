from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import Indicador, Produto, Metas, Registro, Posto
from django.db import IntegrityError
from django.db import models
from django.http import JsonResponse
from django.db.models import Sum, Count, F
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test

def group_required(group_name):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                return render(request, '403.html', status=403)  # Página de acesso negado
        return _wrapped_view
    return decorator

# Página Inicial
def home(request):
    return render(request, 'home.html')

# Indicadores - Lista de Indicadores
@login_required
def indicadores_view(request):
    indicadores = Indicador.objects.all()  # Recupera todos os indicadores
    return render(request, 'indicadores.html', {'indicadores': indicadores})

# Login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redireciona para a página inicial após login
        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas.'})
    return render(request, 'login.html')

# Metas - Lista de Metas
@login_required
def metas_view(request):
    indicadores = Indicador.objects.all()  # Puxa todos os indicadores
    metas = Metas.objects.all()  # Puxa todas as metas
    context = {
        'indicadores': indicadores,
        'metas': metas,
    }
    return render(request, 'metas.html', context)

# Adicionar Indicador - Página para adicionar um indicador
@login_required
def add_indicador(request):
    if request.method == 'POST':
        try:
            nome_indicador = request.POST['nome_indicador']
            descricao = request.POST['descricao']
            frequencia = request.POST['frequencia']
            unidade_medida = request.POST['unidade_medida']

            # Criação de um novo indicador
            Indicador.objects.create(
                nome=nome_indicador,
                descricao=descricao,
                frequencia=frequencia,
                unidade=unidade_medida
            )
            return redirect('indicadores')  # Redireciona para a lista de indicadores

        except IntegrityError:
            return render(request, 'add_indicador.html', {
                'error_message': 'Erro ao salvar o indicador. Verifique os dados informados.'
            })

    return render(request, 'add_indicador.html')

# Adicionar Meta - Página para adicionar uma meta
@login_required
def add_meta(request):
    indicadores = Indicador.objects.all()  # Recupera todos os indicadores para o dropdown
    if request.method == 'POST':
        indicador_id = request.POST.get('indicador')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dt_inicio = request.POST.get('dt_inicio')
        dt_fim = request.POST.get('dt_fim')

        # Certifique-se de que o indicador existe
        indicador = get_object_or_404(Indicador, id=indicador_id)

        # Crie a nova meta
        Metas.objects.create(
            indicador=indicador,
            descricao=descricao,
            valor=valor,
            dt_inicio=dt_inicio,
            dt_fim=dt_fim
        )
        return redirect('metas')  # Redireciona para a lista de metas

    return render(request, 'add_meta.html', {'indicadores': indicadores})

# Administrador - Página do administrador
@login_required
@group_required('Administrador')
def admin_page(request):
    return render(request, 'admin.html')

# Dashboard - Visualização geral
from django.db.models import Sum, Count
from decimal import Decimal
import datetime

@login_required
def dashboard(request):
    # Indicadores com totais agregados
    indicadores = Indicador.objects.annotate(
        total_valor=Sum('registros__valor'),
        frequencia_count=Count('registros')
    ).values('nome_indicador', 'unidade_medida', 'total_valor', 'frequencia_count')

    # Converta os Decimals para float e os None para 0
    indicadores = [
        {
            'nome_indicador': ind['nome_indicador'],
            'unidade_medida': ind['unidade_medida'],
            'total_valor': float(ind['total_valor']) if ind['total_valor'] is not None else 0,
            'frequencia_count': ind['frequencia_count']
        }
        for ind in indicadores
    ]

    # Evolução dos registros por data
    registros_por_data = Registro.objects.values('data_coleta').annotate(
        total=Sum('valor')
    ).order_by('data_coleta')

    # Converta os Decimals para float e data para string
    registros_por_data = [
        {
            'data_coleta': reg['data_coleta'].strftime('%Y-%m-%d'),
            'total': float(reg['total'])
        }
        for reg in registros_por_data
    ]

    context = {
        "indicadores": indicadores,
        "registros_evolucao": registros_por_data,
    }
    return render(request, 'dashboard.html', context)

# Perfil do Usuário
@login_required
def profile(request):
    return render(request, 'profile.html')

# Relatório
@login_required
def rel(request):
    registros = Registro.objects.all()  # Recupera todos os registros
    return render(request, 'rel.html', {'registros': registros})

# Registro de novo usuário
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/login.html', {'form': form})

# Classe de Login Personalizado
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

import csv
from django.http import HttpResponse
from .models import Indicador, Registro
from django.db.models import Sum, Count

@login_required
def export_dashboard(request):
    # Configura o nome do arquivo CSV
    filename = "dashboard_export.csv"

    # Configura o cabeçalho HTTP para download do arquivo
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Cria o escritor CSV
    writer = csv.writer(response)

    # Adiciona o cabeçalho do arquivo CSV
    writer.writerow(['Indicador', 'Unidade de Medida', 'Total Registrado', 'Frequência'])

    # Busca os indicadores e os dados agregados
    indicadores = Indicador.objects.annotate(
        total_valor=Sum('registros__valor'),
        frequencia_count=Count('registros')
    )

    # Adiciona os dados dos indicadores no CSV
    for indicador in indicadores:
        writer.writerow([
            indicador.nome_indicador,
            indicador.unidade_medida,
            indicador.total_valor if indicador.total_valor else 0,
            indicador.frequencia_count
        ])

    # Adiciona uma linha vazia e os dados de evolução (opcional)
    writer.writerow([])
    writer.writerow(['Evolução por Data'])
    writer.writerow(['Data', 'Total'])

    registros_por_data = Registro.objects.values('data_coleta').annotate(
        total=Sum('valor')
    ).order_by('data_coleta')

    for registro in registros_por_data:
        writer.writerow([
            registro['data_coleta'].strftime('%Y-%m-%d'),
            registro['total']
        ])

    return response
@login_required
def indicador_save(request):
    if request.method == "POST":
        nome_indicador = request.POST.get("nome_indicador")
        total = request.POST.get("total")
        frequencia = request.POST.get("frequencia")
        unidade_medida = request.POST.get("unidade_medida")
        descricao = request.POST.get("descricao")

        # Criação do indicador
        Indicador.objects.create(
            nome_indicador=nome_indicador,
            total=total,
            frequencia=frequencia,
            unidade_medida=unidade_medida,
            descricao=descricao,
        )

        # Adiciona mensagem de sucesso
        messages.success(request, "Indicador cadastrado com sucesso!")

        # Redireciona de volta para a página de indicadores
        return redirect("indicadores")
    
@login_required
def metas_save(request):
    if request.method == "POST":
        indicador_id = request.POST.get("indicador")
        descricao = request.POST.get("descricao")
        valor = request.POST.get("valor")
        dt_inicio = request.POST.get("dt_inicio")
        dt_fim = request.POST.get("dt_fim")

        try:
            indicador = get_object_or_404(Indicador, id=indicador_id)
            meta = Metas.objects.create(
                indicador=indicador,
                descricao=descricao,
                valor=valor,
                dt_inicio=dt_inicio,
                dt_fim=dt_fim
            )
            meta.save()
            messages.success(request, "Meta salva com sucesso!")
        except Exception as e:
            messages.error(request, f"Erro ao salvar meta: {str(e)}")
        
        return redirect(reverse('metas'))

    else:
        messages.error(request, "Método inválido.")
        return redirect(reverse('metas'))
    
    # Função para excluir um indicador
@login_required
def indicador_delete(request, id):
    indicador = get_object_or_404(Indicador, id=id)
    indicador.delete()
    messages.success(request, "Indicador excluído com sucesso!")
    return redirect('indicadores')  # Redirecione para a lista de indicadores

# Função para atualizar um indicador
@login_required
def indicador_update(request, id):
    indicador = get_object_or_404(Indicador, id=id)

    if request.method == "POST":
        indicador.nome_indicador = request.POST.get("nome_indicador")
        indicador.total = request.POST.get("total")
        indicador.frequencia = request.POST.get("frequencia")
        indicador.unidade_medida = request.POST.get("unidade_medida")
        indicador.descricao = request.POST.get("descricao")
        indicador.save()
        messages.success(request, "Indicador atualizado com sucesso!")
        return redirect('indicadores')  # Redirecione para a lista de indicadores

    return render(request, "indicador_update.html", {"indicador": indicador})
@login_required
def metas_delete(request, id):
    meta = get_object_or_404(Metas, id=id)
    meta.delete()
    messages.success(request, "Meta excluída com sucesso!")
    return redirect('metas')  # Redireciona para a página de metas
