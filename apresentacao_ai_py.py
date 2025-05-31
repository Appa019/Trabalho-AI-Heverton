import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import json
import os
import io
import re
import unicodedata
from datetime import datetime
import warnings
import logging
import sys
import contextlib
import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
import requests
import pymupdf as fitz
import pikepdf

# Configuração da página
st.set_page_config(
    page_title="IA para Otimização de Processos - CSN Energia",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado com paleta azul escuro e branco
st.markdown("""
<style>
    .main {
        background-color: #ffffff;
    }
    
    .slide-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .slide-title {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .slide-subtitle {
        font-size: 1.5rem;
        opacity: 0.9;
    }
    
    .content-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(30, 58, 138, 0.1);
        border-left: 5px solid #1e3a8a;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 2px solid #1e3a8a;
        margin: 1rem 0;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #64748b;
        font-weight: 500;
    }
    
    .highlight-box {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .navigation-buttons {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 999;
    }
    
    .nav-button {
        background: #1e3a8a;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        margin: 0 5px;
        cursor: pointer;
        font-weight: bold;
        box-shadow: 0 2px 10px rgba(30, 58, 138, 0.3);
    }
    
    .nav-button:hover {
        background: #3b82f6;
        transform: translateY(-2px);
    }
    
    .bullet-point {
        color: #1e3a8a;
        font-size: 1.2rem;
        margin: 0.5rem 0;
        padding-left: 1rem;
    }
    
    .roi-calculator {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 2px solid #1e3a8a;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado da sessão
if 'current_slide' not in st.session_state:
    st.session_state.current_slide = 0

# Definir slides
slides = [
    "Capa",
    "Visão Estratégica",
    "Matriz Esforço x Impacto", 
    "Solução PDFator",
    "Demonstração PDFator",
    "Calculadora ROI",
    "Resultados e Benefícios",
    "Conclusões"
]

# Sidebar para navegação
with st.sidebar:
    st.markdown("### 📋 Navegação")
    for i, slide in enumerate(slides):
        if st.button(f"{i+1}. {slide}", key=f"nav_{i}"):
            st.session_state.current_slide = i

# Funções auxiliares para PDFator
def normalizar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto = texto.lower().strip()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    texto = re.sub(r'[^a-zA-Z0-9]', '', texto)
    return texto

def calcular_custo_api(response):
    try:
        usage = response.usage
        input_tokens = usage.prompt_tokens
        output_tokens = usage.completion_tokens
        preco_input = 0.0005
        preco_output = 0.0015
        custo = (input_tokens * preco_input + output_tokens * preco_output) / 1000
        return custo
    except:
        return 0

# Mapeamento de cobrança (versão resumida para o exemplo)
mapeamento_tipo_cobranca = {
    "Energia elet. adquirida 3": "Encargo",
    "energia elet adquirida 3": "Encargo",
    "DEDUCAO ENERGIA ACL": "Desc. Encargo",
    "DEDUCÃO ENERGIA ACL": "Desc. Encargo",
    "demanda ponta c/desconto": "Demanda",
    "DEMANDA FORA PONTA C/DESC": "Demanda",
    "Contrib llum Publica Municipal": "Contb. Publica",
    "CIP-ILUM PUB PREF MUNICIPAL": "Contb. Publica",
    "UFER PONTA TE": "Reativa",
    "Energia Reativa kWh HFP": "Reativa"
}

# Slides
current_slide = st.session_state.current_slide

if current_slide == 0:  # CAPA
    st.markdown("""
    <div class="slide-header">
        <div class="slide-title">🤖 Inteligência Artificial</div>
        <div class="slide-title">para Otimização de Processos</div>
        <div class="slide-subtitle">Caso de Estudo: CSN Energia - PDFator</div>
        <br>
        <div style="font-size: 1.2rem;">
            Automatização Inteligente de Faturas de Energia<br>
            <em>Transformando dados não estruturados em insights estratégicos</em>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #1e3a8a; text-align: center;">🎯 Objetivo da Apresentação</h3>
            <div class="bullet-point">• Demonstrar aplicação prática de IA em processos industriais</div>
            <div class="bullet-point">• Apresentar o PDFator: solução de automação com IA generativa</div>
            <div class="bullet-point">• Mostrar ROI real e mensurável em operações da CSN Energia</div>
            <div class="bullet-point">• Explorar estratégias de implementação escalável</div>
        </div>
        """, unsafe_allow_html=True)

elif current_slide == 1:  # VISÃO ESTRATÉGICA
    st.markdown("""
    <div class="slide-header">
        <div class="slide-title">🎯 Visão Estratégica</div>
        <div class="slide-subtitle">IA como Catalisador de Eficiência Operacional</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #1e3a8a;">🏭 Sobre a CSN Energia</h3>
            <div class="bullet-point">• Maior consumidora industrial de energia do Brasil</div>
            <div class="bullet-point">• Operações integradas: siderurgia, mineração, energia</div>
            <div class="bullet-point">• Múltiplas unidades com distribuidoras diferentes</div>
            <div class="bullet-point">• Complexidade na gestão de dados energéticos</div>
        </div>
        
        <div class="highlight-box">
            <h4>🎯 Drivers Estratégicos</h4>
            <div style="margin: 1rem 0;">✓ Aumentar receita</div>
            <div style="margin: 1rem 0;">✓ Otimizar custos operacionais</div>
            <div style="margin: 1rem 0;">✓ Maior controle da operação</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #1e3a8a;">⚡ Desafios Identificados</h3>
            <div class="bullet-point">• Faturas em formatos heterogêneos</div>
            <div class="bullet-point">• Processo manual de 30min/fatura</div>
            <div class="bullet-point">• Taxa de erro humano de ~15%</div>
            <div class="bullet-point">• Dificuldade na consolidação de KPIs</div>
        </div>
        
        <div class="content-card">
            <h3 style="color: #1e3a8a;">🤖 Oportunidades com IA</h3>
            <div class="bullet-point">• OCR + IA Generativa para extração</div>
            <div class="bullet-point">• Padronização automática de dados</div>
            <div class="bullet-point">• Redução de 95% no tempo de processo</div>
            <div class="bullet-point">• Precisão superior a 95%</div>
        </div>
        """, unsafe_allow_html=True)

elif current_slide == 2:  # MATRIZ ESFORÇO X IMPACTO
    st.markdown("""
    <div class="slide-header">
        <div class="slide-title">📊 Matriz Esforço x Impacto</div>
        <div class="slide-subtitle">Priorização Estratégica de Projetos de IA</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Dados da matriz
    projetos = {
        'Projeto': ['Análise de Dados de Energia', 'Manutenção Preventiva', 'Previsão de Demanda', 'Monitoramento ESG'],
        'Esforço': [2.0, 2.0, 4.5, 4.0],
        'Impacto': [4.8, 2.0, 4.8, 2.0],
        'Descrição': [
            'PDFator - Automação de faturas', 
            'IA para equipamentos',
            'Previsão com ML',
            'Monitoramento ambiental'
        ]
    }
    
    df_matriz = pd.DataFrame(projetos)
    
    # Criar gráfico da matriz
    fig = px.scatter(df_matriz, 
                     x='Esforço', y='Impacto', 
                     text='Projeto',
                     color='Impacto',
                     size='Impacto',
                     color_continuous_scale=[[0, '#e2e8f0'], [1, '#1e3a8a']])
    
    fig.update_traces(textposition="top center", textfont_size=12, textfont_color="#1e3a8a")
    fig.update_layout(
        title="Matriz de Priorização - Projetos de IA na CSN",
        xaxis_title="Esforço de Implementação",
        yaxis_title="Impacto no Negócio",
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1e3a8a'),
        title_font_size=20,
        height=500
    )
    
    # Adicionar linhas de grade
    fig.add_hline(y=3.5, line_dash="dash", line_color="#64748b", opacity=0.5)
    fig.add_vline(x=3.0, line_dash="dash", line_color="#64748b", opacity=0.5)
    
    # Adicionar anotações dos quadrantes
    fig.add_annotation(x=1.5, y=4.5, text="Alto Impacto<br>Baixo Esforço", 
                      showarrow=False, font_color="#1e3a8a", bgcolor="#f0f9ff")
    fig.add_annotation(x=4.2, y=4.5, text="Alto Impacto<br>Alto Esforço", 
                      showarrow=False, font_color="#1e3a8a", bgcolor="#f0f9ff")
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="highlight-box">
            <h4>🥇 Projeto Piloto Selecionado</h4>
            <strong>Análise de Dados de Energia (PDFator)</strong><br>
            ✓ Alto impacto no negócio<br>
            ✓ Baixo esforço de implementação<br>
            ✓ ROI mensurável e imediato
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="content-card">
            <h4 style="color: #1e3a8a;">📈 Critérios de Avaliação</h4>
            <div class="bullet-point">• Viabilidade técnica</div>
            <div class="bullet-point">• Disponibilidade de dados</div>
            <div class="bullet-point">• Impacto financeiro</div>
            <div class="bullet-point">• Risco de implementação</div>
        </div>
        """, unsafe_allow_html=True)

elif current_slide == 3:  # SOLUÇÃO PDFATOR
    st.markdown("""
    <div class="slide-header">
        <div class="slide-title">🔧 Solução PDFator</div>
        <div class="slide-subtitle">Arquitetura de IA para Processamento Inteligente</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #1e3a8a;">🏗️ Arquitetura Técnica</h3>
            <div class="bullet-point">• <strong>OCR:</strong> PaddleOCR + OpenCV</div>
            <div class="bullet-point">• <strong>IA Generativa:</strong> GPT-3.5-turbo</div>
            <div class="bullet-point">• <strong>Processamento:</strong> Python + Pandas</div>
            <div class="bullet-point">• <strong>Interface:</strong> Streamlit</div>
            <div class="bullet-point">• <strong>Output:</strong> Excel estruturado</div>
        </div>
        
        <div class="content-card">
            <h3 style="color: #1e3a8a;">⚙️ Funcionalidades</h3>
            <div class="bullet-point">• Upload múltiplo (até 80 PDFs)</div>
            <div class="bullet-point">• Tratamento de PDFs protegidos</div>
            <div class="bullet-point">• Categorização automática</div>
            <div class="bullet-point">• Extração de metadados</div>
            <div class="bullet-point">• Relatórios consolidados</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Fluxo do processo
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #1e3a8a;">🔄 Fluxo de Processamento</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Criar fluxograma simples
        processo_steps = pd.DataFrame({
            'Etapa': range(1, 9),
            'Processo': [
                'Upload PDFs',
                'Extração OCR', 
                'IA Generativa',
                'Normalização',
                'Categorização',
                'Validação',
                'Consolidação',
                'Export Excel'
            ],
            'Tempo': ['0s', '10s', '15s', '2s', '3s', '1s', '2s', '1s']
        })
        
        for idx, row in processo_steps.iterrows():
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); 
                        color: white; padding: 0.8rem; margin: 0.3rem 0; 
                        border-radius: 8px; text-align: center;">
                <strong>{row['Etapa']}. {row['Processo']}</strong> 
                <span style="float: right;">~{row['Tempo']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="highlight-box">
            <h4>⚡ Performance</h4>
            <strong>Tempo total: ~34 segundos/fatura</strong><br>
            vs. 30 minutos manual (98.1% redução)
        </div>
        """, unsafe_allow_html=True)

elif current_slide == 4:  # DEMONSTRAÇÃO PDFATOR
    st.markdown("""
    <div class="slide-header">
        <div class="slide-title">🎬 Demonstração PDFator</div>
        <div class="slide-subtitle">Sistema em Funcionamento - Tempo Real</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #1e3a8a;">⚡ PDFator - Extrator de Faturas de Energia</h3>
            <p>Sistema de automação com IA para processamento de faturas de energia elétrica da CSN.</p>
            <br>
            <div class="bullet-point">• Interface web intuitiva e responsiva</div>
            <div class="bullet-point">• Processamento em lote até 80 PDFs</div>
            <div class="bullet-point">• Extração automática com IA generativa</div>
            <div class="bullet-point">• Categorização inteligente de cobranças</div>
            <div class="bullet-point">• Relatórios Excel estruturados</div>
            <div class="bullet-point">• Tratamento de PDFs protegidos</div>
        </div>
        
        <div style="text-align: center; margin: 2rem 0;">
            <a href="https://leitorfaturasv7.streamlit.app/" target="_blank">
                <div style="background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); 
                           color: white; padding: 1.5rem 3rem; border-radius: 15px; 
                           text-decoration: none; display: inline-block; font-size: 1.3rem; 
                           font-weight: bold; box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3);
                           transition: transform 0.3s ease;">
                    🚀 ACESSAR PDFATOR EM TEMPO REAL 🚀
                </div>
            </a>
            <p style="margin-top: 1rem; color: #64748b; font-style: italic;">
                Clique para abrir o sistema funcional em nova aba
            </p>
        </div>
        
        <div class="highlight-box">
            <h4>💡 Como testar o sistema:</h4>
            1. Abra o link do PDFator<br>
            2. Insira sua chave da API OpenAI<br>
            3. Faça upload de PDFs de faturas<br>
            4. Veja a magia da IA acontecer!<br>
            5. Baixe o relatório Excel estruturado
        </div>
    </div>
    
    with col2:
        # Métricas em tempo real
        st.markdown("### 📊 Performance do Sistema")
        
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">98.1%</div>
            <div class="metric-label">Redução de Tempo</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">95%</div>
            <div class="metric-label">Precisão</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">80</div>
            <div class="metric-label">PDFs/Lote</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">6</div>
            <div class="metric-label">Categorias</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Preview da interface
        st.markdown("### 🖥️ Preview da Interface")
        
        # Exemplo visual da categorização
        exemplo_resultado = pd.DataFrame({
            'Categoria': ['Encargo', 'Desc. Encargo', 'Demanda', 'Reativa', 'Contb. Publica'],
            'Valor (R$)': [15420.30, -2340.50, 8750.20, 450.10, 125.30]
        })
        
        fig = px.bar(exemplo_resultado, x='Categoria', y='Valor (R$)', 
                    color='Valor (R$)', 
                    color_continuous_scale=['#ef4444', '#1e3a8a'])
        fig.update_layout(
            title="Exemplo: Categorização Automática",
            plot_bgcolor='white', 
            paper_bgcolor='white',
            height=300,
            font=dict(size=10)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 8px; 
                    border-left: 4px solid #1e3a8a; margin-top: 1rem;">
            <strong>💼 Para a demonstração:</strong><br>
            Use qualquer PDF de fatura de energia elétrica brasileira. 
            O sistema reconhece formatos de todas as principais distribuidoras.
        </div>
        """, unsafe_allow_html=True)

elif current_slide == 5:  # CALCULADORA ROI
    st.markdown("""
    <div class="slide-header">
        <div class="slide-title">💰 Calculadora de ROI</div>
        <div class="slide-subtitle">Simulação de Economia em Tempo Real</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="roi-calculator">
        <h3 style="color: #1e3a8a; text-align: center;">🧮 Simulador de Retorno sobre Investimento</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### ⚙️ Parâmetros de Entrada")
        
        # Inputs para cálculo
        num_faturas = st.slider("Número de faturas processadas/mês", 50, 1000, 500, 50)
        custo_hora_analista = st.slider("Custo/hora do analista (R$)", 60, 120, 80, 10)
        tempo_manual_min = st.slider("Tempo manual por fatura (min)", 20, 45, 30, 5)
        precisao_manual = st.slider("Precisão manual (%)", 80, 95, 85, 5)
        
        # Parâmetros fixos do sistema
        tempo_pdfator_min = 1.5
        precisao_pdfator = 95
        custo_sistema_mensal = 450
        
    with col2:
        st.markdown("### 📊 Resultados Calculados")
        
        # Cálculos
        tempo_manual_total_horas = (num_faturas * tempo_manual_min) / 60
        tempo_pdfator_total_horas = (num_faturas * tempo_pdfator_min) / 60
        
        economia_tempo_horas = tempo_manual_total_horas - tempo_pdfator_total_horas
        economia_monetaria = economia_tempo_horas * custo_hora_analista
        economia_liquida = economia_monetaria - custo_sistema_mensal
        
        roi_percentual = ((economia_liquida / custo_sistema_mensal) * 100) if custo_sistema_mensal > 0 else 0
        payback_dias = (custo_sistema_mensal / (economia_monetaria / 30)) if economia_monetaria > 0 else 0
        
        # Exibir métricas
        col2_1, col2_2 = st.columns(2)
        
        with col2_1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">R$ {economia_liquida:,.0f}</div>
                <div class="metric-label">Economia Líquida/Mês</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{roi_percentual:.0f}%</div>
                <div class="metric-label">ROI Mensal</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2_2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{economia_tempo_horas:.0f}h</div>
                <div class="metric-label">Economia de Tempo/Mês</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{payback_dias:.0f}</div>
                <div class="metric-label">Payback (dias)</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Gráfico de comparação
    st.markdown("### 📈 Análise Comparativa Anual")
    
    meses = list(range(1, 13))
    economia_acumulada = [economia_liquida * m for m in meses]
    investimento_acumulado = [custo_sistema_mensal * m for m in meses]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=meses, y=economia_acumulada, 
                           mode='lines+markers', name='Economia Acumulada',
                           line=dict(color='#1e3a8a', width=3)))
    fig.add_trace(go.Scatter(x=meses, y=investimento_acumulado,
                           mode='lines+markers', name='Investimento Acumulado',
                           line=dict(color='#ef4444', width=3)))
    
    fig.update_layout(
        title=f"Projeção Anual - {num_faturas} faturas/mês",
        xaxis_title="Mês",
        yaxis_title="Valor (R$)",
        plot_bgcolor='white',
        paper_bgcolor='white',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Resumo executivo
    st.markdown(f"""
    <div class="highlight-box">
        <h4>📋 Resumo Executivo</h4>
        <strong>Cenário: {num_faturas} faturas/mês</strong><br><br>
        ✓ Economia anual: <strong>R$ {economia_liquida * 12:,.0f}</strong><br>
        ✓ Tempo economizado/ano: <strong>{economia_tempo_horas * 12:.0f} horas</strong><br>
        ✓ Melhoria na precisão: <strong>{precisao_pdfator - precisao_manual}%</strong><br>
        ✓ ROI anual: <strong>{roi_percentual * 12:.0f}%</strong>
    </div>
    """, unsafe_allow_html=True)

elif current_slide == 6:  # RESULTADOS E BENEFÍCIOS
    st.markdown("""
    <div class="slide-header">
        <div class="slide-title">🎯 Resultados e Benefícios</div>
        <div class="slide-subtitle">Impacto Mensurável da IA nos Processos</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">R$ 220k</div>
            <div class="metric-label">Economia Anual</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">2.840h</div>
            <div class="metric-label">Tempo Economizado/Ano</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">95%</div>
            <div class="metric-label">Precisão da IA</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">7 dias</div>
            <div class="metric-label">Payback</div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #1e3a8a;">📈 Benefícios Quantitativos</h3>
            <div class="bullet-point">• <strong>98.1%</strong> redução no tempo de processamento</div>
            <div class="bullet-point">• <strong>10%</strong> melhoria na precisão dos dados</div>
            <div class="bullet-point">• <strong>4.900%</strong> ROI anual</div>
            <div class="bullet-point">• <strong>80 PDFs</strong> processados simultaneamente</div>
            <div class="bullet-point">• <strong>Zero</strong> erros de digitação</div>
        </div>
        
        <div class="content-card">
            <h3 style="color: #1e3a8a;">⚡ Benefícios Qualitativos</h3>
            <div class="bullet-point">• Padronização de processos</div>
            <div class="bullet-point">• Rastreabilidade completa</div>
            <div class="bullet-point">• Disponibilidade 24/7</div>
            <div class="bullet-point">• Escalabilidade automática</div>
            <div class="bullet-point">• Liberação para atividades estratégicas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Gráfico comparativo antes/depois
        comparacao_data = pd.DataFrame({
            'Métrica': ['Tempo/Fatura', 'Precisão', 'Custo/Fatura', 'Capacidade/Dia'],
            'Antes (Manual)': [30, 85, 40, 16],
            'Depois (IA)': [1.5, 95, 0.9, 1280],
            'Unidade': ['min', '%', 'R, 'faturas']
        })
        
        fig = go.Figure()
        
        x = comparacao_data['Métrica']
        fig.add_trace(go.Bar(name='Processo Manual', x=x, y=comparacao_data['Antes (Manual)'],
                           marker_color='#ef4444', opacity=0.8))
        fig.add_trace(go.Bar(name='Com IA (PDFator)', x=x, y=comparacao_data['Depois (IA)'],
                           marker_color='#1e3a8a', opacity=0.8))
        
        fig.update_layout(
            title="Comparativo: Antes vs Depois da IA",
            barmode='group',
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=400,
            font=dict(color='#1e3a8a')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Evolução temporal
        st.markdown("""
        <div class="highlight-box">
            <h4>🚀 Roadmap de Expansão</h4>
            <strong>Fase 1:</strong> PDFator (Concluído)<br>
            <strong>Fase 2:</strong> Integração Power BI<br>
            <strong>Fase 3:</strong> API para ERP<br>
            <strong>Fase 4:</strong> IA Preditiva
        </div>
        """, unsafe_allow_html=True)

elif current_slide == 7:  # CONCLUSÕES
    st.markdown("""
    <div class="slide-header">
        <div class="slide-title">🎊 Conclusões</div>
        <div class="slide-subtitle">IA como Acelerador de Transformação Digital</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="content-card">
            <h3 style="color: #1e3a8a;">🎯 Principais Aprendizados</h3>
            <div class="bullet-point">• <strong>IA Prática:</strong> Soluções reais para problemas específicos</div>
            <div class="bullet-point">• <strong>ROI Mensurável:</strong> Resultados tangíveis em semanas</div>
            <div class="bullet-point">• <strong>Escalabilidade:</strong> De piloto a solução corporativa</div>
            <div class="bullet-point">• <strong>Adoção Gradual:</strong> Mudança cultural sustentável</div>
            <div class="bullet-point">• <strong>Tecnologia Acessível:</strong> Ferramentas disponíveis hoje</div>
        </div>
        
        <div class="content-card">
            <h3 style="color: #1e3a8a;">🔬 Fatores Críticos de Sucesso</h3>
            <div class="bullet-point">• Escolha do caso de uso certo (matriz esforço x impacto)</div>
            <div class="bullet-point">• Prototipação rápida e iterativa</div>
            <div class="bullet-point">• Validação constante com usuários finais</div>
            <div class="bullet-point">• Gestão de mudanças estruturada</div>
            <div class="bullet-point">• Monitoramento contínuo de performance</div>
        </div>
        
        <div class="content-card">
            <h3 style="color: #1e3a8a;">🚀 Próximos Passos</h3>
            <div class="bullet-point">• Expansão para outros tipos de documentos</div>
            <div class="bullet-point">• Integração com sistemas corporativos</div>
            <div class="bullet-point">• IA preditiva para demanda energética</div>
            <div class="bullet-point">• Automação de relatórios ESG</div>
            <div class="bullet-point">• Criação de centro de excelência em IA</div>
        </div>
    </div>
    
    with col2:
        st.markdown("""
        <div class="highlight-box">
            <h4>💡 Lições Aprendidas</h4>
            <br>
            <strong>"A IA não substitui humanos, potencializa capacidades"</strong>
            <br><br>
            ✓ Start small, think big<br>
            ✓ Dados são o novo petróleo<br>
            ✓ Iteração rápida > Perfeição<br>
            ✓ ROI deve ser mensurável<br>
            ✓ Adoção é sobre pessoas
        </div>
        """, unsafe_allow_html=True)
        
        # Gráfico de impacto
        impacto_areas = pd.DataFrame({
            'Área': ['Eficiência', 'Qualidade', 'Custos', 'Inovação', 'Pessoas'],
            'Impacto': [95, 90, 85, 80, 75]
        })
        
        fig = px.bar(impacto_areas, x='Impacto', y='Área', orientation='h',
                    color='Impacto', color_continuous_scale=['#f0f9ff', '#1e3a8a'])
        fig.update_layout(
            title="Impacto da IA por Área",
            plot_bgcolor='white',
            paper_bgcolor='white',
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
        <div class="content-card">
            <h4 style="color: #1e3a8a; text-align: center;">🏆 Resultado Final</h4>
            <div style="text-align: center; font-size: 1.2rem; color: #1e3a8a;">
                <strong>De 30 minutos para 1.5 minutos</strong><br>
                <strong>De 85% para 95% de precisão</strong><br>
                <strong>ROI de 4.900% ao ano</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%); 
                color: white; padding: 2rem; border-radius: 15px; 
                text-align: center; margin: 2rem 0;">
        <h2>🤖 A IA está transformando a indústria</h2>
        <h3>O futuro é agora. A questão não é "se", mas "quando" sua organização vai adotar.</h3>
        <br>
        <div style="font-size: 1.2rem;">
            <strong>PDFator: Prova de que IA pode gerar valor real, mensurável e imediato</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Navegação
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("⬅️ Anterior", disabled=(current_slide == 0)):
        st.session_state.current_slide = max(0, current_slide - 1)
        st.rerun()

with col2:
    st.markdown(f"""
    <div style="text-align: center; padding: 10px; background: #f8fafc; 
                border-radius: 10px; border: 2px solid #1e3a8a;">
        <strong>Slide {current_slide + 1} de {len(slides)}</strong><br>
        <em>{slides[current_slide]}</em>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if st.button("Próximo ➡️", disabled=(current_slide == len(slides) - 1)):
        st.session_state.current_slide = min(len(slides) - 1, current_slide + 1)
        st.rerun()

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 1rem; 
            color: #64748b; border-top: 1px solid #e2e8f0;">
    <strong>Apresentação: IA para Otimização de Processos - CSN Energia</strong><br>
    Desenvolvido com Streamlit • Dados baseados em caso real • 2025
</div>
""", unsafe_allow_html=True)