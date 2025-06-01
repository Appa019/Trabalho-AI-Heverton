import streamlit as st
import random
import time
import datetime
import math
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Calculadora do Amor Quântica",
    page_icon="❤️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS customizado para estilização
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #ffebee 0%, #fce4ec 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #ffebee 0%, #fce4ec 100%);
    }
    
    .love-title {
        color: #e91e63;
        text-align: center;
        font-size: 3rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .result-container {
        background: linear-gradient(135deg, #f8bbd0 0%, #f48fb1 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .calculation-box {
        background: #1e1e1e;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        max-height: 400px;
        overflow-y: auto;
        border: 2px solid #333;
    }
    
    .quantum-equation {
        color: #00ffff;
        font-weight: bold;
    }
    
    .matrix-equation {
        color: #ff6b6b;
        font-weight: bold;
    }
    
    .integral-equation {
        color: #4ecdc4;
        font-weight: bold;
    }
    
    @keyframes float {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
    }
    
    .floating-heart {
        position: fixed;
        font-size: 2rem;
        animation: float 6s linear infinite;
        pointer-events: none;
    }
</style>
""", unsafe_allow_html=True)

class QuantumLoveCalculator:
    def __init__(self):
        self.greek_letters = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω']
        self.quantum_operators = ['Ĥ', 'Ψ', '∇²', '∂²', '⟨ψ|', '|ψ⟩', '†', '⊗', '⊕']
        self.mathematical_symbols = ['∫', '∑', '∏', '∂', '∇', '∆', '∞', '≈', '≠', '≤', '≥', '⊂', '⊃', '⊆', '⊇', '∈', '∉']
        self.complex_functions = ['sinh', 'cosh', 'tanh', 'sech', 'csch', 'coth', 'arcsinh', 'arccosh', 'arctanh', 'Γ', 'ζ', 'Β']
        self.quantum_states = ['|0⟩', '|1⟩', '|+⟩', '|-⟩', '|i⟩', '|-i⟩', '|↑⟩', '|↓⟩', '|→⟩', '|←⟩']
        
    def generate_quantum_equation(self) -> str:
        """Gera equações quânticas complexas"""
        equations = [
            f"Ĥ|ψ⟩ = E|ψ⟩ where E = {random.uniform(1.0, 100.0):.6f} ℏω",
            f"⟨ψ₁|ψ₂⟩ = ∫ ψ₁*({random.choice(self.greek_letters)})ψ₂({random.choice(self.greek_letters)})d{random.choice(self.greek_letters)} = {random.uniform(-1, 1):.8f}",
            f"∇²ψ + (2m/ℏ²)[E - V({random.choice(self.greek_letters)})]ψ = 0",
            f"[Ĥ, p̂] = iℏ∇V = {random.uniform(-10, 10):.4f} × 10⁻³⁴ J·s",
            f"ρ̂ = ∑ₙ pₙ|n⟩⟨n| = {random.uniform(0, 1):.6f}|↑⟩⟨↑| + {random.uniform(0, 1):.6f}|↓⟩⟨↓|"
        ]
        return f'<span class="quantum-equation">⚛️ {random.choice(equations)}</span>'
    
    def generate_tensor_calculation(self) -> str:
        """Gera cálculos tensoriais avançados"""
        tensors = [
            f"Rμν - ½gμνR + Λgμν = (8πG/c⁴)Tμν",
            f"∂μTμν = 0 ⟹ ∇·T = {random.uniform(-100, 100):.4f}",
            f"Fμν = ∂μAν - ∂νAμ = {random.uniform(-50, 50):.6f} Tesla·m",
            f"Gμν = Rμν - ½gμνR = {random.uniform(-1000, 1000):.8f} m⁻²",
            f"εμνρσ∂μ∂νAρ = {random.uniform(-10, 10):.6f} × 10⁻¹² Wb/m²"
        ]
        return f'<span class="matrix-equation">📊 {random.choice(tensors)}</span>'
    
    def generate_complex_integral(self) -> str:
        """Gera integrais multidimensionais complexas"""
        var1, var2, var3 = random.choices(self.greek_letters, k=3)
        func = random.choice(['sin', 'cos', 'exp', 'ln', 'sinh', 'cosh'])
        
        integrals = [
            f"∭∭∭ {func}({var1}²+{var2}²+{var3}²) d{var1}d{var2}d{var3} = {random.uniform(0, 1000):.8f}",
            f"∮∮ F⃗·dS⃗ = ∭(∇·F⃗)dV = {random.uniform(-500, 500):.6f}",
            f"∫₋∞^∞ e^(-{var1}²/2σ²) d{var1} = σ√(2π) = {random.uniform(1, 10):.6f}",
            f"∫∫ᴅ {func}({var1},{var2}) dA = ∫₀^(2π) ∫₀^R r·{func}(r,θ) dr dθ = {random.uniform(0, 100):.8f}",
            f"∫ₒ^∞ x^n e^(-{var1}x) dx = n!/{var1}^(n+1) = {random.uniform(0.001, 100):.8f}"
        ]
        return f'<span class="integral-equation">∫ {random.choice(integrals)}</span>'
    
    def generate_matrix_operation(self) -> str:
        """Gera operações matriciais complexas"""
        size = random.choice([3, 4, 5])
        det_val = random.uniform(-1000, 1000)
        eigenval = random.uniform(-10, 10)
        
        operations = [
            f"det(A{size}×{size}) = {det_val:.6f}, tr(A) = {random.uniform(-50, 50):.4f}",
            f"A⁻¹ exists iff det(A) ≠ 0, ||A||₂ = {random.uniform(1, 100):.6f}",
            f"λₘₐₓ(A) = {eigenval:.6f}, cond(A) = {random.uniform(1, 1000):.4f}",
            f"A ⊗ B = [{random.randint(1,9)} × {random.randint(1,9)} matrix], rank = {random.randint(1, size)}",
            f"exp(A) = I + A + A²/2! + ... = ||{random.uniform(0.1, 10):.6f}||"
        ]
        return f'<span class="matrix-equation">📐 {random.choice(operations)}</span>'
    
    def generate_fourier_analysis(self) -> str:
        """Gera análises de Fourier complexas"""
        freq = random.uniform(0.1, 100)
        amplitude = random.uniform(0.1, 50)
        
        fourier_eqs = [
            f"F(ω) = ∫₋∞^∞ f(t)e^(-iωt) dt = {amplitude:.6f}e^(i{random.uniform(0, 2*math.pi):.4f})",
            f"f(t) = (1/2π) ∫₋∞^∞ F(ω)e^(iωt) dω, ||f||₂ = {random.uniform(1, 100):.6f}",
            f"Parseval: ∫|f(t)|² dt = (1/2π)∫|F(ω)|² dω = {random.uniform(10, 1000):.6f}",
            f"DFT: X[k] = ∑ₙ₌₀^(N-1) x[n]e^(-i2πkn/N), |X[{random.randint(0,63)}]| = {amplitude:.6f}",
            f"PSD: S(ω) = |F(ω)|²/T = {random.uniform(0.001, 100):.8f} W/Hz"
        ]
        return f'<span class="quantum-equation">🌊 {random.choice(fourier_eqs)}</span>'
    
    def generate_statistical_mechanics(self) -> str:
        """Gera equações de mecânica estatística"""
        temp = random.uniform(100, 500)
        energy = random.uniform(1, 50)
        
        stat_mech = [
            f"Z = ∑ᵢ e^(-Eᵢ/kT) = e^(-βF), β = 1/kT = {1/(1.38e-23 * temp):.2e} J⁻¹",
            f"⟨E⟩ = -∂ln(Z)/∂β = {energy:.6f} eV, Cv = ∂⟨E⟩/∂T = {random.uniform(0.1, 10):.4f} J/K",
            f"S = k ln(Ω) = -k ∑ᵢ pᵢ ln(pᵢ) = {random.uniform(0, 100):.6f} J/K",
            f"f(E) = 1/(e^((E-μ)/kT) + 1), μ = {random.uniform(-5, 5):.4f} eV",
            f"P = -(∂F/∂V)ₜ = nkT/V - an²/V² = {random.uniform(0.1, 10):.6f} atm"
        ]
        return f'<span class="integral-equation">🔥 {random.choice(stat_mech)}</span>'
    
    def generate_string_theory_calculations(self) -> str:
        """Gera cálculos de teoria das cordas"""
        coupling = random.uniform(0.1, 2.0)
        
        string_eqs = [
            f"S = -1/(2πα') ∫ d²σ √(-h) h^(αβ) ∂α X^μ ∂β X^ν gμν = {random.uniform(-1000, 1000):.8f}",
            f"Compactification: M₄ × K₆ → M₁₀, Vol(K₆) = {random.uniform(1e-30, 1e-20):.2e} l_p⁶",
            f"β-function: βgμν = α'Rμν + α'²(∇²Rμν + ...) = {random.uniform(-10, 10):.6f}",
            f"Dilaton field: ⟨e^φ⟩ = gs = {coupling:.6f}, λstring = gs² = {coupling**2:.8f}",
            f"AdS₅/CFT₄: ∫ d⁵x √g R = ∫ d⁴x Tr(F²μν) = {random.uniform(0, 1000):.6f}",
            f"Calabi-Yau: ∫Y₆ Ω ∧ Ω̄ = 0, h^(1,1) = {random.randint(1, 100)}, h^(2,1) = {random.randint(1, 200)}",
            f"D-brane tension: Tp = 1/((2π)^p ls^(p+1) gs) = {random.uniform(1e10, 1e20):.2e} GeV^(p+1)"
        ]
        return f'<span class="quantum-equation">🧬 {random.choice(string_eqs)}</span>'
    
    def generate_machine_learning_calculations(self) -> str:
        """Gera cálculos de machine learning"""
        accuracy = random.uniform(0.85, 0.99)
        loss = random.uniform(0.001, 0.5)
        
        ml_eqs = [
            f"∇L(θ) = (1/m)Σᵢ∇θℓ(hθ(xᵢ), yᵢ), learning_rate = {random.uniform(0.001, 0.1):.6f}",
            f"Cross-entropy: L = -Σyᵢlog(ŷᵢ) = {loss:.8f}, accuracy = {accuracy:.4f}",
            f"Backprop: ∂L/∂w = ∂L/∂a × ∂a/∂z × ∂z/∂w, chain rule applied",
            f"Transformer: Attention(Q,K,V) = softmax(QKᵀ/√dk)V, heads = {random.randint(8, 64)}",
            f"LSTM: ft = σ(Wf·[ht-1,xt] + bf), forget gate activated",
            f"CNN: feature_maps = {random.randint(32, 512)}, kernel_size = {random.choice([3, 5, 7])}×{random.choice([3, 5, 7])}",
            f"GAN: min_G max_D V(D,G) = 𝔼[log D(x)] + 𝔼[log(1-D(G(z)))]",
            f"VAE: ELBO = 𝔼[log p(x|z)] - KL(q(z|x)||p(z)) = {random.uniform(-1000, 0):.4f}"
        ]
        return f'<span class="integral-equation">🤖 {random.choice(ml_eqs)}</span>'
    
    def generate_quantum_computing_calculations(self) -> str:
        """Gera cálculos de computação quântica"""
        qubits = random.choice([16, 32, 64, 128, 256, 512, 1024])
        fidelity = random.uniform(0.95, 0.999)
        
        quantum_comp = [
            f"Shor's algorithm: O((log N)³), factoring {random.randint(100, 10000)}-bit RSA",
            f"Grover's search: O(√N) iterations, database_size = 2^{random.randint(20, 40)}",
            f"Quantum gate: U = e^(-iHt/ℏ), fidelity = {fidelity:.6f}, error_rate = {1-fidelity:.8f}",
            f"Entanglement: |Ψ⟩ = (|00⟩ + |11⟩)/√2, concurrence C = {random.uniform(0.5, 1):.6f}",
            f"Decoherence: T₁ = {random.uniform(10, 1000):.2f}μs, T₂ = {random.uniform(5, 500):.2f}μs",
            f"QAOA: |γ,β⟩ = e^(-iβĤB)e^(-iγĤC)|+⟩^⊗n, layers p = {random.randint(1, 10)}",
            f"VQE: ⟨Ψ(θ)|Ĥ|Ψ(θ)⟩, ground_state_energy = {random.uniform(-100, 0):.6f} Ha"
        ]
        return f'<span class="quantum-equation">💻 {random.choice(quantum_comp)}</span>'
    
    def generate_cosmology_calculations(self) -> str:
        """Gera cálculos cosmológicos"""
        hubble = random.uniform(65, 75)
        redshift = random.uniform(0.1, 10)
        
        cosmology_eqs = [
            f"Friedmann: H² = (8πG/3)ρ - kc²/a², H₀ = {hubble:.2f} km/s/Mpc",
            f"Dark energy: ΩΛ = {random.uniform(0.65, 0.75):.4f}, w = {random.uniform(-1.2, -0.8):.4f}",
            f"CMB anisotropy: ΔT/T = {random.uniform(1e-5, 1e-4):.2e}, ℓ_peak = {random.randint(200, 300)}",
            f"Inflation: φ̈ + 3Hφ̇ + V'(φ) = 0, e-folding N = {random.randint(50, 80)}",
            f"Nucleosynthesis: Ωb h² = {random.uniform(0.020, 0.025):.5f}, Yp = {random.uniform(0.24, 0.26):.4f}",
            f"Structure formation: σ₈ = {random.uniform(0.7, 0.9):.4f}, ns = {random.uniform(0.95, 1.0):.4f}",
            f"Supernova: μ = 5log₁₀(dL/10pc), z = {redshift:.4f}, dL = {random.uniform(100, 10000):.2f} Mpc"
        ]
        return f'<span class="matrix-equation">🌌 {random.choice(cosmology_eqs)}</span>'
    
    def generate_cryptographic_calculations(self) -> str:
        """Gera cálculos criptográficos"""
        key_size = random.choice([128, 256, 512, 1024, 2048, 4096])
        entropy = random.uniform(100, 256)
        
        crypto_eqs = [
            f"RSA: n = p×q, φ(n) = (p-1)(q-1), key_size = {key_size} bits",
            f"AES-{random.choice([128, 192, 256])}: S-box σ: 𝔽₂₈ → 𝔽₂₈, rounds = {random.randint(10, 14)}",
            f"SHA-{random.choice([256, 384, 512])}: H: {{0,1}}* → {{0,1}}^{random.choice([256, 384, 512])}, collision-resistant",
            f"Elliptic curve: y² ≡ x³ + ax + b (mod p), |E| = {random.randint(2**50, 2**100)}",
            f"Discrete log: g^x ≡ h (mod p), p = {random.randint(2**50, 2**100)}-bit prime",
            f"Entropy: H(X) = -Σp(x)log₂p(x) = {entropy:.4f} bits"
        ]
        return f'<span class="matrix-equation">🔐 {random.choice(crypto_eqs)}</span>'
    
    def get_random_calculation(self) -> str:
        """Retorna um cálculo aleatório de todas as categorias disponíveis"""
        generators = [
            self.generate_quantum_equation,
            self.generate_tensor_calculation,
            self.generate_complex_integral,
            self.generate_matrix_operation,
            self.generate_fourier_analysis,
            self.generate_statistical_mechanics,
            self.generate_string_theory_calculations,
            self.generate_machine_learning_calculations,
            self.generate_quantum_computing_calculations,
            self.generate_cosmology_calculations,
            self.generate_cryptographic_calculations
        ]
        return random.choice(generators)()

def initialize_session_state():
    """Inicializa o estado da sessão"""
    if 'stage' not in st.session_state:
        st.session_state.stage = 'input'
    if 'nome1' not in st.session_state:
        st.session_state.nome1 = ''
    if 'nome2' not in st.session_state:
        st.session_state.nome2 = ''
    if 'data1' not in st.session_state:
        st.session_state.data1 = None
    if 'data2' not in st.session_state:
        st.session_state.data2 = None
    if 'calculations' not in st.session_state:
        st.session_state.calculations = []

def input_stage():
    """Estágio de entrada de dados"""
    st.markdown('<h1 class="love-title">💕 Calculadora do Amor Quântica 💕</h1>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("love_form"):
                st.markdown("### 📝 Dados para Análise Quântica")
                
                nome1 = st.text_input("🧑 Seu Nome:", placeholder="Digite seu nome")
                nome2 = st.text_input("👥 Nome do(a) Parceiro(a):", placeholder="Digite o nome do(a) parceiro(a)")
                
                col_date1, col_date2 = st.columns(2)
                with col_date1:
                    data1 = st.date_input("📅 Sua Data de Nascimento:")
                with col_date2:
                    data2 = st.date_input("📅 Data de Nascimento do(a) Parceiro(a):")
                
                submitted = st.form_submit_button("🔬 Iniciar Análise Quântica", use_container_width=True)
                
                if submitted and nome1 and nome2 and data1 and data2:
                    st.session_state.nome1 = nome1
                    st.session_state.nome2 = nome2
                    st.session_state.data1 = data1
                    st.session_state.data2 = data2
                    st.session_state.stage = 'calculating'
                    st.rerun()
                elif submitted:
                    st.error("❌ Por favor, preencha todos os campos!")

def calculating_stage():
    """Estágio de cálculo com animações"""
    st.markdown('<h1 class="love-title">🔬 Análise Quântica em Andamento</h1>', unsafe_allow_html=True)
    
    # Barra de progresso
    progress_bar = st.progress(0)
    status_text = st.empty()
    calculation_container = st.empty()
    
    calculator = QuantumLoveCalculator()
    
    # Container para os cálculos
    with calculation_container.container():
        st.markdown('<div class="calculation-box">', unsafe_allow_html=True)
        calc_display = st.empty()
        
        calculations = []
        
        # Simulação de cálculos em tempo real
        stages = [
            "🔬 Inicializando analisador quântico multidimensional...",
            "⚛️ Calculando sobreposição de estados emocionais em 11 dimensões...",
            "🌌 Analisando entrelaçamento quântico dos padrões neurais...",
            "📊 Processando matrizes de compatibilidade tensoriais...",
            "🧮 Executando transformadas de Fourier nos dados temporais...",
            "🎯 Aplicando mecânica estatística aos padrões comportamentais...",
            "🧬 Decodificando sequências genéticas de compatibilidade...",
            "💰 Calculando derivativos de amor através de modelos Black-Scholes...",
            "🌪️ Simulando sistemas caóticos de atração romântica...",
            "🔐 Aplicando criptografia quântica aos sentimentos...",
            "🤖 Treinando redes neurais profundas de 500 camadas...",
            "📐 Computando geometria algébrica dos corações entrelaçados...",
            "🕸️ Executando algoritmos de grafos em redes de relacionamento...",
            "⚙️ Verificando complexidade computacional P vs NP do amor...",
            "📦 Aplicando teoria de categorias aos functores afetivos...",
            "🌊 Renormalizando campos quânticos de paixão...",
            "🎲 Executando Monte Carlo com 10^9 simulações...",
            "🧠 Processando arquiteturas Transformer de última geração...",
            "🌌 Calculando constante cosmológica do universo romântico...",
            "🔮 Finalizando análise hiper-multidimensional...",
            "✨ Compilando resultado através de inteligência artificial quântica..."
        ]
        
        for i, stage_text in enumerate(stages):
            status_text.text(stage_text)
            progress_bar.progress((i + 1) / len(stages))
            
            # Gerar múltiplos cálculos por estágio (mais cálculos!)
            for _ in range(random.randint(8, 15)):
                new_calc = calculator.get_random_calculation()
                calculations.append(new_calc)
                
                # Mostrar últimos 20 cálculos
                display_calcs = calculations[-20:] if len(calculations) > 20 else calculations
                calc_text = "<br>".join(display_calcs)
                calc_display.markdown(f'<div style="font-family: monospace; font-size: 0.8em;">{calc_text}</div>', unsafe_allow_html=True)
                
                time.sleep(random.uniform(0.05, 0.2))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Após completar os cálculos
    time.sleep(1)
    st.session_state.stage = 'result'
    st.rerun()

def result_stage():
    """Estágio de resultado"""
    st.markdown('<h1 class="love-title">🎊 Resultado da Análise Quântica</h1>', unsafe_allow_html=True)
    
    # Determinar o resultado baseado nos nomes (sempre o primeiro nome)
    winner = st.session_state.nome1
    loser = st.session_state.nome2
    
    # Container do resultado
    with st.container():
        st.markdown(f'''
        <div class="result-container">
            <h2 style="color: #880e4f; margin-bottom: 1rem;">💖 RESULTADO OFICIAL 💖</h2>
            <h1 style="font-size: 2.5rem; color: #e91e63; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                {winner} ama mais {loser}! 
            </h1>
            <p style="font-size: 1.2rem; color: #880e4f; margin-top: 1rem;">
                Nossa análise quântica multidimensional revelou este resultado com 99.97% de precisão!
            </p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Estatísticas adicionais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🔬 Precisão Quântica", "99.97%", "0.03%")
    
    with col2:
        compatibility = random.randint(87, 99)
        st.metric("💕 Compatibilidade", f"{compatibility}%", f"{random.randint(1, 8)}%")
    
    with col3:
        quantum_entanglement = random.uniform(0.92, 0.998)
        st.metric("⚛️ Entrelaçamento", f"{quantum_entanglement:.5f}", "0.0012")
    
    # Métricas adicionais em uma segunda linha
    col4, col5, col6 = st.columns(3)
    
    with col4:
        neural_score = random.uniform(8.5, 9.9)
        st.metric("🧠 Score Neural", f"{neural_score:.2f}/10", f"{random.uniform(0.1, 0.5):.2f}")
    
    with col5:
        chaos_factor = random.uniform(0.15, 0.35)
        st.metric("🌪️ Fator Caos", f"{chaos_factor:.4f}", f"{random.uniform(-0.01, 0.01):.4f}")
    
    with col6:
        tensor_correlation = random.uniform(0.88, 0.97)
        st.metric("📊 Correlação Tensorial", f"{tensor_correlation:.4f}", "0.0023")
    
    # Botão para nova análise
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔄 Nova Análise", use_container_width=True):
            # Reset session state
            for key in ['stage', 'nome1', 'nome2', 'data1', 'data2', 'calculations']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
    
    # Efeito de confetes (simulado com emojis)
    st.markdown("## 🎉🎊💖🎈✨🌹💕🎉🎊💖🎈✨🌹💕🎉🎊💖🎈✨🌹💕")

def main():
    """Função principal"""
    initialize_session_state()
    
    # Navegação baseada no estágio
    if st.session_state.stage == 'input':
        input_stage()
    elif st.session_state.stage == 'calculating':
        calculating_stage()
    elif st.session_state.stage == 'result':
        result_stage()

if __name__ == "__main__":
    main()
