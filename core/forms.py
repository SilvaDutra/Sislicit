# Arquivo: core/forms.py (100% Completo e Corrigido)

from django import forms
from django.db import models # <-- IMPORTAÇÃO ADICIONADA AQUI
from .models import Processo, Orgao, Secretaria, Fornecedor, Responsavel # Adicionei Secretaria

class OrgaoForm(forms.ModelForm):
    class Meta:
        model = Orgao
        fields = ['nome', 'cnpj', 'endereco', 'telefone', 'email', 'logo']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control' if field_name != 'logo' else 'form-control-file'

class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['razao_social', 'nome_fantasia', 'cnpj', 'telefone', 'email']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        if 'cnpj' in self.fields:
            self.fields['cnpj'].widget.attrs['placeholder'] = 'Digite CNPJ e aguarde'

class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = Responsavel
        fields = ['nome', 'matricula', 'cargo', 'secretaria']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ProcessoForm(forms.ModelForm):
    class Meta:
        model = Processo
        fields = ['numero_processo', 'orgao_responsavel', 'secretaria_responsavel', 'responsavel_demanda', 'modalidade', 'status', 'objeto', 'valor_estimado', 'vigencia_meses', 'justificativa', 'descricao_detalhada_objeto']
        widgets = {'objeto': forms.Textarea(attrs={'rows': 2}), 'justificativa': forms.Textarea(attrs={'rows': 4}), 'descricao_detalhada_objeto': forms.Textarea(attrs={'rows': 4})}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ETPForm(forms.ModelForm):
    class Meta:
        model = Processo
        fields = [
            'etp_responsavel_elaboracao','justificativa','etp_pca_texto',
            'etp_texto_estimativa_quantidades','etp_texto_levantamento_mercado',
            'etp_estimativa_metodologia','etp_analise_fornecedores_detalhe',
            'etp_requisitos_texto_geral','etp_requisitos_marcas_texto',
            'etp_requisitos_amostra_texto','etp_requisitos_tecnicos_detalhe',
            'etp_requisitos_capacitacao_detalhe','valor_estimado',
            'etp_descricao_solucao_texto','etp_solucao_proposta_detalhe',
            'etp_analise_alternativas_detalhe','etp_justificativa_parcelamento_texto',
            'etp_resultados_pretendidos_texto','etp_providencias_texto',
            'etp_contratacoes_correlatas_texto','etp_alinhamento_estrategico_texto',
            'etp_impactos_ambientais_texto','etp_autoridade_competente',
            'secretaria_responsavel','etp_gestor_contrato','etp_fiscal_tecnico',
            'etp_fiscal_administrativo','etp_prazo_execucao','vigencia_meses',
            'etp_justificativa_prazo','modalidade','etp_criterio_julgamento',
            'etp_justificativa_modalidade_criterio','etp_dotacao_programa_trabalho',
            'etp_dotacao_natureza_despesa','etp_dotacao_fonte_recursos',
            'etp_lista_anexos_texto','etp_justificativa_contratacao',
        ]
        # Widgets agora funcionarão corretamente com 'models.TextField'
        widgets = {
            field_name: forms.Textarea(attrs={'rows': 3})
            for field_name in fields # Itera sobre os campos definidos acima
            # Acessa o tipo do campo diretamente pelo modelo Processo
            if hasattr(Processo, field_name) and isinstance(Processo._meta.get_field(field_name), models.TextField)
        }
        widgets['justificativa'] = forms.Textarea(attrs={'rows': 5})
        widgets['descricao_detalhada_objeto'] = forms.Textarea(attrs={'rows': 5})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'