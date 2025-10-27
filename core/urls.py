# Arquivo: core/urls.py (COMPLETO E CORRIGIDO - VERSÃO FINAL 10.0)

from django.urls import path
from . import views

urlpatterns = [
    # Página inicial
    path('', views.dashboard, name='dashboard'),
    path('painel/', views.dashboard, name='painel'), 

    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Processos
    path('processos/', views.processo_list, name='processo_list'),
    path('processos/<int:pk>/', views.processo_detail, name='processo_detail'), 
    path('processos/novo/', views.processo_create, name='processo_create'),
    path('processos/<int:pk>/editar/', views.processo_update, name='processo_update'),
    path('processos/<int:pk>/deletar/', views.processo_delete, name='processo_delete'),
    path('processos/<int:pk>/exportar-pdf/', views.exportar_andamento_pdf, name='exportar_andamento_pdf'),
    path('processos/<int:pk>/etp/', views.processo_etp_form, name='processo_etp_form'),
    path('processos/<int:pk>/documentos/', views.processo_documentos, name='processo_documentos'),
    # ADICIONADA A URL FALTANTE (DO CHECKLIST):
    path('processos/salvar-etapa/', views.salvar_etapa_historico, name='salvar_etapa_historico'), # <--- URL FALTANTE

    # Relatórios
    path('relatorios/', views.relatorio_processos, name='relatorio_processos'), 
    path('relatorios/fases-excel/', views.relatorio_fases_excel, name='relatorio_fases_excel'),
    path('relatorios/fases-pdf/', views.relatorio_fases_pdf, name='relatorio_fases_pdf'),
    path('relatorios/exportar-csv/', views.exportar_processos_csv, name='exportar_processos_csv'), 
    path('relatorios/exportar-pdf/', views.exportar_processos_pdf, name='exportar_processos_pdf'), 
    
    # Documentos (Geral)
    path('documentos/', views.documentos_list, name='documentos_list'),
    path('documentos/gerar-dfd/<int:processo_id>/', views.gerar_dfd, name='gerar_dfd'),
    path('documentos/gerar-etp/<int:processo_id>/', views.gerar_etp, name='gerar_etp'),
    path('documentos/gerar-tr/<int:processo_id>/', views.gerar_tr, name='gerar_tr'),
    path('documentos/download/<int:documento_id>/', views.download_documento, name='download_documento'),

    # ==== CRUD ÓRGÃOS ==== 
    path('orgaos/', views.orgao_list, name='orgao_list'), 
    path('orgaos/novo/', views.orgao_create, name='orgao_create'), 
    path('orgaos/<int:pk>/editar/', views.orgao_update, name='orgao_update'), 
    path('orgaos/<int:pk>/deletar/', views.orgao_delete, name='orgao_delete'), 

    # ==== CRUD FORNECEDORES ==== 
    path('fornecedores/', views.fornecedor_list, name='fornecedor_list'), 
    path('fornecedores/novo/', views.fornecedor_create, name='fornecedor_create'), 
    path('fornecedores/<int:pk>/editar/', views.fornecedor_update, name='fornecedor_update'), 
    path('fornecedores/<int:pk>/deletar/', views.fornecedor_delete, name='fornecedor_delete'), 

    # ==== CRUD RESPONSÁVEIS ==== 
    path('responsaveis/', views.responsavel_list, name='responsavel_list'), 
    path('responsaveis/novo/', views.responsavel_create, name='responsavel_create'), 
    path('responsaveis/<int:pk>/editar/', views.responsavel_update, name='responsavel_update'), 
    path('responsaveis/<int:pk>/deletar/', views.responsavel_delete, name='responsavel_delete'), 
]