# Arquivo: core/models.py (COMPLETO COM MODELO DE DOCUMENTOS)

from django.db import models

class Orgao(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome do Órgão")
    logo = models.ImageField(upload_to='logos/', null=True, blank=True, verbose_name="Logotipo")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    endereco = models.CharField(max_length=255, verbose_name="Endereço")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    email = models.EmailField(verbose_name="E-mail de Contato")
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Órgão"
        verbose_name_plural = "Órgãos Públicos"


class Secretaria(models.Model):
    orgao = models.ForeignKey(Orgao, on_delete=models.CASCADE, related_name='secretarias', verbose_name="Órgão")
    nome = models.CharField(max_length=200, verbose_name="Nome da Secretaria")
    
    def __str__(self):
        return f"{self.nome} ({self.orgao.nome})"
    
    class Meta:
        verbose_name = "Secretaria"
        verbose_name_plural = "Secretarias"
        unique_together = ('orgao', 'nome')


class Responsavel(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome Completo")
    matricula = models.CharField(max_length=50, verbose_name="Matrícula", unique=True)
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    secretaria = models.ForeignKey(Secretaria, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Secretaria de Lotação")
    
    def __str__(self):
        return f"{self.nome} ({self.cargo})"
    
    class Meta:
        verbose_name = "Responsável"
        verbose_name_plural = "Responsáveis"


class Fornecedor(models.Model):
    razao_social = models.CharField(max_length=200, verbose_name="Razão Social")
    nome_fantasia = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nome Fantasia")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefone")
    email = models.EmailField(verbose_name="E-mail")
    
    def __str__(self):
        return self.razao_social
    
    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"


class Processo(models.Model):
    STATUS_CHOICES = [
        ('FASE_INTERNA', 'Fase Interna'),
        ('PUBLICADO', 'Publicado'),
        ('AGUARDANDO_PROPOSTAS', 'Aguardando Propostas'),
        ('EM_ANALISE', 'Em Análise'),
        ('HOMOLOGADO', 'Homologado'),
        ('CANCELADO', 'Cancelado')
    ]
    
    MODALIDADE_CHOICES = [
        ('PREGAO', 'Pregão'),
        ('CONCORRENCIA', 'Concorrência'),
        ('CONCURSO', 'Concurso'),
        ('LEILAO', 'Leilão'),
        ('DIALOGO_COMPETITIVO', 'Diálogo Competitivo'),
        ('DISPENSA', 'Dispensa de Licitação'),
        ('INEXIGIBILIDADE', 'Inexigibilidade de Licitação')
    ]
    
    CRITERIO_JULGAMENTO_CHOICES = [
        ('MENOR_PRECO', 'Menor Preço'),
        ('MAIOR_DESCONTO', 'Maior Desconto'),
        ('MELHOR_TECNICA', 'Melhor Técnica ou Conteúdo Artístico'),
        ('TECNICA_PRECO', 'Técnica e Preço'),
        ('MAIOR_RETORNO', 'Maior Retorno Econômico')
    ]

    # Campos Gerais / DFD
    numero_processo = models.CharField(max_length=50, unique=True, verbose_name="Número do Processo")
    orgao_responsavel = models.ForeignKey(Orgao, on_delete=models.PROTECT, verbose_name="Órgão Responsável")
    secretaria_responsavel = models.ForeignKey(Secretaria, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Unidade Requisitante / Setor Demandante")
    responsavel_demanda = models.ForeignKey(Responsavel, on_delete=models.SET_NULL, null=True, blank=True, related_name='processos_demandados', verbose_name="Responsável pela Demanda (DFD)")
    objeto = models.TextField(verbose_name="Objeto da Contratação (Resumido)")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='FASE_INTERNA', verbose_name="Status")
    modalidade = models.CharField(max_length=30, choices=MODALIDADE_CHOICES, verbose_name="Modalidade Sugerida")
    data_abertura = models.DateField(auto_now_add=True, verbose_name="Data de Abertura")
    valor_estimado = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Valor Estimado Total")
    justificativa = models.TextField(verbose_name="1. Descrição da Necessidade (DFD/ETP)", blank=True)
    descricao_detalhada_objeto = models.TextField(verbose_name="3.1. Objeto da Contratação Detalhado (DFD/ETP)", blank=True)
    vigencia_meses = models.IntegerField(verbose_name="8. Vigência Contratual (em meses)", null=True, blank=True)

    # ==== CAMPOS ESPECÍFICOS DO ETP ====
    # IDENTIFICAÇÃO
    etp_responsavel_elaboracao = models.ForeignKey(Responsavel, on_delete=models.SET_NULL, null=True, blank=True, related_name='processos_elaborados_etp', verbose_name="Responsável pela Elaboração (ETP)")
    
    # 2. PCA
    etp_pca_texto = models.TextField(verbose_name="2. Previsão no PCA", blank=True, default="Este órgão não elaborou Plano de Contratações Anual para este ano, motivo pelo qual deixo de indicar a previsão desta contratação neste tópico.")
    
    # 3. ESTIMATIVA QUANTIDADES
    etp_texto_estimativa_quantidades = models.TextField(verbose_name="3. Estimativa das Quantidades (Texto)", blank=True, default="Foi emitido relatório de consumo dos últimos 12 meses de todas as repartições deste órgão público, a fim de identificar os quantitativos de produtos consumidos por esta Administração.\nAlém disso, foi enviado ofício para todas as repartições que utilizam esse produto, a fim de indagar se haverá aumento de consumo em algum item específico, bem como se há algum produto extra a ser considerado para a próxima compra.\nEm que pese os levantamentos acima referidos, mensurar sua quantidade exata para uso durante o período de 12 meses não se mostra possível.\nDiante disso, opta-se por realizar pregão na modalidade registro de preços.")
    
    # 4. LEVANTAMENTO MERCADO
    etp_texto_levantamento_mercado = models.TextField(verbose_name="4. Levantamento de Mercado (Texto)", blank=True, default="Considerando que não há soluções mercadológicas a serem consideradas para a aquisição desse objeto, deixo de fazer este levantamento, especialmente porque se trata de uma compra de baixa complexidade e não há outros meios de adquirir estes itens, a não ser pela compra desses produtos com fornecedores que trabalham neste ramo.")
    etp_estimativa_metodologia = models.TextField(verbose_name="6. Metodologia da Estimativa de Preços", blank=True)
    etp_analise_fornecedores_detalhe = models.TextField(verbose_name="4.2. Análise de Fornecedores Detalhada (ETP)", blank=True)
    
    # 5. REQUISITOS
    etp_requisitos_texto_geral = models.TextField(verbose_name="5. Requisitos da Contratação (Texto Introdutório)", blank=True, default="Para esta aquisição, serão exigidos os seguintes requisitos para a contratação:")
    etp_requisitos_marcas_texto = models.TextField(verbose_name="5. Requisitos: Indicação de Marcas (Texto)", blank=True, default="A fim de selecionar um fornecedor que possa atender as especificações mínimas descritas neste estudo e atendam a demanda desta Administração, foram realizadas pesquisas de mercado para verificar quais são as marcas que possuem melhor custo-benefício, com base em critérios técnicos, qualidade comprovada, durabilidade, assistência técnica disponível na região e compatibilidade com as necessidades específicas do objeto licitado.\nA indicação de marcas de referência busca assegurar a aquisição de produtos que atendam aos padrões mínimos de desempenho e eficiência, sem, contudo, restringir a competitividade, uma vez que permite a apresentação de produtos equivalentes que atendam às mesmas especificações técnicas.\nAssim, garante-se a transparência e a objetividade do processo licitatório, resguardando o interesse público e a economicidade.")
    etp_requisitos_amostra_texto = models.TextField(verbose_name="5. Requisitos: Amostra (Texto)", blank=True, default="A exigência de apresentação de amostra no processo licitatório visa garantir que os produtos ofertados atendam integralmente às especificações técnicas e aos padrões de qualidade estabelecidos no termo de referência ou no edital.\nEssa medida é fundamental para assegurar a conformidade dos itens contratados com as necessidades da Administração Pública, minimizando riscos de aquisição de materiais ou bens inadequados.\nA apresentação de amostras permite:\nVerificação da Qualidade: Avaliar se o produto ofertado possui características técnicas, materiais e acabamento compatíveis com os critérios exigidos.\nConformidade com as Especificações: Assegurar que o item atende plenamente aos requisitos estabelecidos, evitando divergências entre o que foi ofertado e o que será entregue.\nRedução de Riscos: Prevenir problemas relacionados à entrega de itens de qualidade inferior ou incompatíveis com o objeto da licitação, promovendo maior eficiência e economicidade.\nDessa forma, a exigência de amostra é um instrumento que contribui para a lisura e eficiência do processo licitatório, resguardando o interesse público e garantindo a qualidade na aquisição dos bens ou materiais necessários.")
    etp_requisitos_tecnicos_detalhe = models.TextField(verbose_name="3.2. Requisitos Técnicos Detalhados (ETP)", blank=True)
    etp_requisitos_capacitacao_detalhe = models.TextField(verbose_name="3.3. Requisitos de Capacitação Técnica Detalhados (ETP)", blank=True)
    
    # 5 (parte 2). JUSTIFICATIVA CONTRATAÇÃO
    etp_justificativa_contratacao = models.TextField(verbose_name="5. Justificativa da Contratação (ETP)", blank=True)
    
    # 7. DESCRIÇÃO SOLUÇÃO
    etp_descricao_solucao_texto = models.TextField(verbose_name="7. Descrição da Solução como um Todo (Texto)", blank=True, default="Considerando os levantamentos realizados neste Estudo Técnico Preliminar, chegou-se à conclusão de que não há outras soluções mercadológicas a serem consideradas, a não ser a compra desses produtos por intermédio de fornecedores.\nOs quantitativos, em que pese terem sido levantados por intermédio de relatórios e ofícios para as demais secretarias requisitantes, ainda sim podem sofrer alteração no decorrer do ano, razão pela qual optou-se por realizar um pregão na modalidade registro de preços.")
    etp_solucao_proposta_detalhe = models.TextField(verbose_name="6.1. Solução Proposta Detalhada (ETP)", blank=True)
    etp_analise_alternativas_detalhe = models.TextField(verbose_name="6.2. Análise de Alternativas Detalhada (ETP)", blank=True)
    
    # 8. JUSTIFICATIVA PARCELAMENTO
    etp_justificativa_parcelamento_texto = models.TextField(verbose_name="8. Justificativas para Parcelamento (Texto)", blank=True, default="Em se tratando de aquisição de produtos divisíveis, os quais serão comprados por intermédio de um pregão na modalidade registro de preços e que há um rol extenso de materiais diferentes que devem ser fornecidos, opta-se por executar a licitação dividida em itens, uma vez que ampliará a competitividade e não limitará os fornecedores que não possuem determinados itens para fornecimento.")
    
    # 9. RESULTADOS PRETENDIDOS
    etp_resultados_pretendidos_texto = models.TextField(verbose_name="9. Demonstrativo dos Resultados Pretendidos (Texto)", blank=True, default="Como não há soluções comparativas em relação a essa compra, não há como demonstrar os resultados pretendidos em detrimento de outras hipóteses.")
    
    # 10. PROVIDÊNCIAS
    etp_providencias_texto = models.TextField(verbose_name="10. Providências a serem Adotadas (Texto)", blank=True, default="Não há providências a serem adotadas pela Administração nesta compra.")
    
    # 11. CONTRATAÇÕES CORRELATAS
    etp_contratacoes_correlatas_texto = models.TextField(verbose_name="11. Contratações Correlatas/Interdependentes (Texto)", blank=True, default="Não há contratações correlatas e/ou interdependentes para essa aquisição.")
    etp_alinhamento_estrategico_texto = models.TextField(verbose_name="11. Alinhamento ao Planejamento (Texto)", blank=True)
    
    # 12. IMPACTOS AMBIENTAIS
    etp_impactos_ambientais_texto = models.TextField(verbose_name="12. Possíveis Impactos Ambientais (Texto)", blank=True, default="Não há medidas sustentáveis ou impactos ambientais a serem considerados nessa contratação.")
    
    # 14. APROVAÇÃO E ASSINATURA
    etp_autoridade_competente = models.ForeignKey(Responsavel, on_delete=models.SET_NULL, null=True, blank=True, related_name='processos_aprovados_etp', verbose_name="Autoridade Competente (Aprovação ETP)")
    
    # 15. ÁREA REQUISITANTE E FISCALIZAÇÃO
    etp_gestor_contrato = models.CharField(max_length=200, verbose_name="2. Gestor do Contrato (ETP)", blank=True)
    etp_fiscal_tecnico = models.CharField(max_length=200, verbose_name="2. Fiscal Técnico (ETP)", blank=True)
    etp_fiscal_administrativo = models.CharField(max_length=200, verbose_name="2. Fiscal Administrativo (ETP)", blank=True)
    
    # 8 (parte 2). PRAZO EXECUÇÃO E VIGÊNCIA
    etp_prazo_execucao = models.IntegerField(verbose_name="8. Prazo de Execução (em meses) (ETP)", null=True, blank=True)
    etp_justificativa_prazo = models.TextField(verbose_name="8. Justificativa do Prazo (ETP)", blank=True)
    
    # 9 (parte 2). MODALIDADE E CRITÉRIO
    etp_criterio_julgamento = models.CharField(max_length=30, choices=CRITERIO_JULGAMENTO_CHOICES, verbose_name="9. Critério de Julgamento (ETP)", blank=True)
    etp_justificativa_modalidade_criterio = models.TextField(verbose_name="9. Justificativa da Modalidade e Critério (ETP)", blank=True)
    
    # 16. DOTAÇÃO
    etp_dotacao_programa_trabalho = models.CharField(max_length=100, verbose_name="16. Dotação: Programa de Trabalho", blank=True)
    etp_dotacao_natureza_despesa = models.CharField(max_length=100, verbose_name="16. Dotação: Natureza da Despesa", blank=True)
    etp_dotacao_fonte_recursos = models.CharField(max_length=100, verbose_name="16. Dotação: Fonte de Recursos", blank=True)
    
    # 17. ANEXOS
    etp_lista_anexos_texto = models.TextField(verbose_name="17. Anexos (Texto)", blank=True)

    def __str__(self):
        return f"{self.numero_processo} - {self.get_modalidade_display()}"

    class Meta:
        verbose_name = "Processo"
        verbose_name_plural = "Processos"


class HistoricoProcesso(models.Model):
    ETAPAS_CHOICES = [
        ('DFD', 'Documento de formalização da demanda'),
        ('ETP', 'Estudo Técnico Preliminar (ETP)'),
        ('PESQUISA_PRECOS', 'Pesquisa de preços do mercado'),
        ('DOTACAO', 'Dotação orçamentária'),
        ('MAPA_RISCOS', 'Mapa de riscos, quando exigido'),
        ('TERMO_REF', 'Termo de referência ou projeto básico'),
        ('JUSTIFICATIVA', 'Justificativa'),
        ('PARECER_TECNICO_JURIDICO', 'Parecer da área técnica e/ou jurídica'),
        ('PARECER_CONTROLE_INTERNO', 'Parecer Controle Interno'),
        ('PEDIDO_RATIFICACAO', 'Pedido de Ratificação'),
        ('RATIFICACAO', 'Ratificação'),
        ('AUTORIZACAO', 'Autorização da autoridade competente para o início'),
        ('EDITAL', 'Edital de licitação, incluindo anexos'),
        ('PUBLICACAO_AVISO', 'Publicação do aviso de licitação'),
        ('RECEBIMENTO_PROPOSTAS', 'Recebimento das propostas e documentos de habilitação'),
        ('ATA_SESSAO', 'Ata/súmula de sessão pública'),
        ('PLANILHA_CLASSIFICACAO', 'Planilha de classificação das propostas'),
        ('DOCS_HABILITACAO', 'Documentos apresentados para habilitação'),
        ('PARECERES_FASE_EXTERNA', 'Pareceres técnicos e jurídicos sobre propostas/habilitação'),
        ('RECURSOS', 'Registros de recursos administrativos'),
        ('JULGAMENTO_RECURSOS', 'Ata(s) de julgamento dos recursos'),
        ('ADJUDICACAO', 'Adjudicação do objeto ao licitante vencedor'),
        ('HOMOLOGACAO', 'Homologação final do resultado'),
    ]
    
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='historico')
    etapa = models.CharField(max_length=50, choices=ETAPAS_CHOICES)
    data_conclusao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Histórico de Etapa do Processo"
        verbose_name_plural = "Históricos de Etapas do Processo"
        unique_together = ('processo', 'etapa')
    
    def __str__(self):
        return f"{self.processo.numero_processo} - {self.get_etapa_display()}"


# ==== NOVO MODELO: DOCUMENTOS ====
class Documento(models.Model):
    TIPO_CHOICES = [
        ('DFD', 'Documento de Formalização da Demanda'),
        ('ETP', 'Estudo Técnico Preliminar'),
        ('TR', 'Termo de Referência'),
    ]
    
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='documentos', verbose_name="Processo")
    tipo = models.CharField(max_length=3, choices=TIPO_CHOICES, verbose_name="Tipo de Documento")
    arquivo = models.FileField(upload_to='documentos/%Y/%m/', verbose_name="Arquivo Gerado")
    data_geracao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Geração")
    gerado_por = models.CharField(max_length=200, verbose_name="Gerado por", blank=True)
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.processo.numero_processo}"
    
    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ['-data_geracao']