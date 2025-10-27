# Arquivo: core/admin.py (Completo e Atualizado)

from django.contrib import admin
from .models import Orgao, Secretaria, Fornecedor, Processo, Responsavel

class OrgaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cnpj', 'email', 'telefone')
    search_fields = ('nome', 'cnpj')

class SecretariaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'orgao')
    search_fields = ('nome',)
    list_filter = ('orgao',)

# ================= NOVA CLASSE ADMIN PARA RESPONSAVEL =================
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'cargo', 'secretaria')
    search_fields = ('nome', 'matricula', 'cargo')
    list_filter = ('secretaria',)

class FornecedorAdmin(admin.ModelAdmin):
    list_display = ('razao_social', 'cnpj', 'email')
    search_fields = ('razao_social', 'cnpj')
    class Media:
        js = ('core/js/cnpj_lookup.js',)

class ProcessoAdmin(admin.ModelAdmin):
    list_display = ('numero_processo', 'orgao_responsavel', 'secretaria_responsavel', 'responsavel_demanda', 'modalidade', 'status')
    search_fields = ('numero_processo', 'objeto')
    list_filter = ('status', 'modalidade', 'orgao_responsavel', 'secretaria_responsavel')

admin.site.register(Orgao, OrgaoAdmin)
admin.site.register(Secretaria, SecretariaAdmin)
admin.site.register(Responsavel, ResponsavelAdmin) # <-- Registro do novo modelo
admin.site.register(Fornecedor, FornecedorAdmin)
admin.site.register(Processo, ProcessoAdmin)