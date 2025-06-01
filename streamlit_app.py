import streamlit as st
import time
import random
import datetime
import html

# Configuração da página
st.set_page_config(
    page_title="Calculadora do Amor",
    page_icon="❤️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personalizado
st.markdown("""
<style>
    .main {
        background-color: #ffebee;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .container {
        background-color: white;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        padding: 30px;
        margin: 20px 0;
    }
    h1 {
        color: #e91e63;
        text-align: center;
        margin-bottom: 30px;
    }
    .result {
        font-size: 24px;
        margin: 30px 0;
        padding: 20px;
        background-color: #f8bbd0;
        border-radius: 10px;
        color: #880e4f;
        text-align: center;
    }
    .heart {
        color: #e91e63;
        font-size: 30px;
        display: inline-block;
        animation: pulse 1.5s infinite;
    }
    .calculation-area {
        font-family: 'Courier New', monospace;
        background-color: #f5f5f5;
        border-radius: 5px;
        padding: 15px;
        height: 300px;
        overflow: auto;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #e91e63;
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 16px;
        width: 100%;
        transition: background-color 0.3s;
    }
    .stButton>button:hover {
        background-color: #c2185b;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# Caracteres especiais para cálculos avançados
special_chars = ['∫', '∑', '∏', '∂', '∇', '∆', 'λ', 'θ', 'Ω', 'Φ', '∞', '≈', '≠', '≤', '≥', '⊂', '⊃', '⊆', '⊇', '⊕', '⊗']
greek_letters = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω']

# Função para gerar cálculos aleatórios avançados
def generate_random_calculation():
    # Escolher tipo de cálculo aleatoriamente
    calc_type = random.randint(0, 4)
    
    if calc_type == 0:
        # Cálculo com integrais
        func = random.choice(greek_letters)
        var1 = random.choice(greek_letters)
        var2 = random.choice(greek_letters)
        limits = random.randint(1, 100)
        return f"∫<sub>{limits}</sub><sup>{limits*2}</sup> {func}({var1}) d{var2} = {(random.random() * 1000):.4f}"
    
    elif calc_type == 1:
        # Equação diferencial
        diff_var = random.choice(greek_letters)
        diff_func = random.choice(greek_letters)
        order = random.randint(1, 3)
        coeff = (random.random() * 10)
        return f"d<sup>{order}</sup>{diff_func}/d{diff_var}<sup>{order}</sup> + {coeff:.2f}{diff_func} = {(random.random() * 100):.4f}"
    
    elif calc_type == 2:
        # Matriz
        matrix_size = random.randint(2, 3)
        matrix = "⎡"
        for i in range(matrix_size):
            matrix += " "
            for j in range(matrix_size):
                matrix += str(random.randint(0, 99)) + " "
            matrix += ("⎢" if i < matrix_size - 1 else "⎣")
        matrix += " det = " + f"{(random.random() * 1000):.2f}"
        return matrix
    
    elif calc_type == 3:
        # Série
        series_var = random.choice(greek_letters)
        series_limit = random.randint(10, 30)
        return f"∑<sub>n=1</sub><sup>{series_limit}</sup> {series_var}<sub>n</sub> = {(random.random() * 10000):.2f}"
    
    else:
        # Expressão complexa
        terms = random.randint(2, 4)
        expr = ""
        for i in range(terms):
            coef = (random.random() * 100)
            variable = random.choice(greek_letters)
            power = random.randint(1, 5)
            expr += f"{coef:.2f}{variable}<sup>{power}</sup>"
            if i < terms - 1:
                expr += random.choice([" + ", " - ", " × ", " ÷ "])
        expr += f" = {(random.random() * 100000):.4f}"
        return expr

# Inicialização do estado da sessão
if 'page' not in st.session_state:
    st.session_state.page = 'form'
if 'calculations' not in st.session_state:
    st.session_state.calculations = []
if 'progress' not in st.session_state:
    st.session_state.progress = 0

# Função para mudar para a página de cálculo
def go_to_calculating():
    st.session_state.page = 'calculating'
    st.session_state.calculations = []
    st.session_state.progress = 0
    st.session_state.start_time = time.time()

# Função para mudar para a página de resultado
def go_to_result():
    st.session_state.page = 'result'

# Página do formulário
if st.session_state.page == 'form':
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h1>Calculadora do Amor</h1>', unsafe_allow_html=True)
    
    with st.form("love_form"):
        col1, col2 = st.columns(2)
        with col1:
            nome1 = st.text_input("Seu Nome:", key="nome1")
        with col2:
            nome2 = st.text_input("Nome do(a) Parceiro(a):", key="nome2")
        
        col3, col4 = st.columns(2)
        with col3:
            data1 = st.date_input("Sua Data de Aniversário:", key="data1")
        with col4:
            data2 = st.date_input("Data de Aniversário do(a) Parceiro(a):", key="data2")
        
        submitted = st.form_submit_button("Calcular Amor")
        if submitted:
            if nome1 and nome2:
                st.session_state.nome1 = nome1
                st.session_state.nome2 = nome2
                st.session_state.data1 = data1
                st.session_state.data2 = data2
                go_to_calculating()
            else:
                st.error("Por favor, preencha todos os campos.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Página de cálculo
elif st.session_state.page == 'calculating':
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h1>Calculando Compatibilidade</h1>', unsafe_allow_html=True)
    
    # Barra de progresso
    progress_bar = st.progress(st.session_state.progress)
    
    # Área de cálculos
    st.markdown('<div class="calculation-area" id="calculationArea">', unsafe_allow_html=True)
    for calc in st.session_state.calculations:
        st.markdown(calc, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Lógica para atualizar cálculos e progresso
    elapsed_time = time.time() - st.session_state.start_time
    
    if elapsed_time <= 15:  # 15 segundos de simulação
        # Atualizar progresso
        st.session_state.progress = min(elapsed_time / 15, 1.0)
        progress_bar.progress(st.session_state.progress)
        
        # Adicionar novo cálculo
        if len(st.session_state.calculations) < 100:  # Limitar número de cálculos para evitar lentidão
            st.session_state.calculations.append(generate_random_calculation() + "<br><br>")
        
        # Recarregar a página para atualização
        time.sleep(0.1)
        st.rerun()
    else:
        # Tempo acabou, ir para resultado
        go_to_result()
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Página de resultado
elif st.session_state.page == 'result':
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.markdown('<h1>Resultado da Análise</h1>', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="result">
        <span class="heart">❤️</span> 
        Pedro ama mais a Ana 
        <span class="heart">❤️</span>
    </div>
    <p style="text-align: center;">Nossa análise avançada de compatibilidade revelou este resultado surpreendente!</p>
    ''', unsafe_allow_html=True)
    
    if st.button("Fazer Nova Análise"):
        st.session_state.page = 'form'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
