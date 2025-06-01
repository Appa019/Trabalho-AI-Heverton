from flask import Flask, render_template, request, redirect, url_for
import random
import time
import datetime
import os

app = Flask(__name__)

# Garantir que as pastas necessárias existam
os.makedirs('templates', exist_ok=True)
os.makedirs('static/css', exist_ok=True)
os.makedirs('static/js', exist_ok=True)

# Criar os templates HTML
index_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora do Amor</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #ffebee;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            padding: 30px;
            width: 90%;
            max-width: 500px;
        }
        h1 {
            color: #e91e63;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
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
        button:hover {
            background-color: #c2185b;
        }
        .hearts {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
    </style>
</head>
<body>
    <div class="hearts" id="hearts"></div>
    <div class="container">
        <h1>Calculadora do Amor</h1>
        <form action="/calcular" method="post">
            <div class="form-group">
                <label for="nome1">Seu Nome:</label>
                <input type="text" id="nome1" name="nome1" required>
            </div>
            <div class="form-group">
                <label for="nome2">Nome do(a) Parceiro(a):</label>
                <input type="text" id="nome2" name="nome2" required>
            </div>
            <div class="form-group">
                <label for="data1">Sua Data de Aniversário:</label>
                <input type="date" id="data1" name="data1" required>
            </div>
            <div class="form-group">
                <label for="data2">Data de Aniversário do(a) Parceiro(a):</label>
                <input type="date" id="data2" name="data2" required>
            </div>
            <button type="submit">Calcular Amor</button>
        </form>
    </div>

    <script>
        // Animação de corações flutuantes
        function createHeart() {
            const heart = document.createElement('div');
            heart.innerHTML = '❤️';
            heart.style.position = 'absolute';
            heart.style.fontSize = Math.random() * 20 + 10 + 'px';
            heart.style.left = Math.random() * 100 + 'vw';
            heart.style.top = '-20px';
            heart.style.opacity = Math.random() * 0.5 + 0.5;
            heart.style.animation = `fall ${Math.random() * 5 + 5}s linear`;
            
            document.getElementById('hearts').appendChild(heart);
            
            setTimeout(() => {
                heart.remove();
            }, 10000);
        }

        // Criar corações a cada 1 segundo
        setInterval(createHeart, 1000);

        // Adicionar animação CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fall {
                to {
                    transform: translateY(100vh) rotate(360deg);
                }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>"""

calculando_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculando Compatibilidade</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #ffebee;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }
        .container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            padding: 30px;
            width: 90%;
            max-width: 500px;
            text-align: center;
        }
        h1 {
            color: #e91e63;
            margin-bottom: 20px;
        }
        .calculation-area {
            font-family: 'Courier New', monospace;
            background-color: #f5f5f5;
            border-radius: 5px;
            padding: 15px;
            height: 200px;
            overflow: auto;
            margin-bottom: 20px;
            text-align: left;
        }
        .progress {
            height: 20px;
            background-color: #f5f5f5;
            border-radius: 10px;
            margin-bottom: 20px;
            overflow: hidden;
        }
        .progress-bar {
            height: 100%;
            background-color: #e91e63;
            width: 0%;
            transition: width 15s linear;
        }
        .loading-text {
            margin-bottom: 20px;
            color: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Calculando Compatibilidade</h1>
        <div class="progress">
            <div class="progress-bar" id="progressBar"></div>
        </div>
        <p class="loading-text">Analisando dados e calculando compatibilidade...</p>
        <div class="calculation-area" id="calculationArea"></div>
    </div>

    <script>
        // Dados do formulário
        const nome1 = "{{ nome1 }}";
        const nome2 = "{{ nome2 }}";
        const data1 = "{{ data1 }}";
        const data2 = "{{ data2 }}";
        
        // Área de cálculos
        const calculationArea = document.getElementById('calculationArea');
        const progressBar = document.getElementById('progressBar');
        
        // Caracteres especiais para cálculos avançados
        const specialChars = ['∫', '∑', '∏', '∂', '∇', '∆', 'λ', 'θ', 'Ω', 'Φ', '∞', '≈', '≠', '≤', '≥', '⊂', '⊃', '⊆', '⊇', '⊕', '⊗'];
        const greekLetters = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ', 'ι', 'κ', 'λ', 'μ', 'ν', 'ξ', 'ο', 'π', 'ρ', 'σ', 'τ', 'υ', 'φ', 'χ', 'ψ', 'ω'];
        
        // Função para gerar cálculos aleatórios avançados
        function generateRandomCalculation() {
            // Escolher tipo de cálculo aleatoriamente
            const calcType = Math.floor(Math.random() * 5);
            
            switch(calcType) {
                case 0:
                    // Cálculo com integrais
                    const func = getRandomGreekLetter();
                    const var1 = getRandomGreekLetter();
                    const var2 = getRandomGreekLetter();
                    const limits = Math.floor(Math.random() * 100);
                    return `∫<sub>${limits}</sub><sup>${limits*2}</sup> ${func}(${var1}) d${var2} = ${(Math.random() * 1000).toFixed(4)}`;
                
                case 1:
                    // Equação diferencial
                    const diffVar = getRandomGreekLetter();
                    const diffFunc = getRandomGreekLetter();
                    const order = Math.floor(Math.random() * 3) + 1;
                    const coeff = (Math.random() * 10).toFixed(2);
                    return `d<sup>${order}</sup>${diffFunc}/d${diffVar}<sup>${order}</sup> + ${coeff}${diffFunc} = ${(Math.random() * 100).toFixed(4)}`;
                
                case 2:
                    // Matriz
                    const matrixSize = Math.floor(Math.random() * 2) + 2;
                    let matrix = "⎡";
                    for (let i = 0; i < matrixSize; i++) {
                        matrix += " ";
                        for (let j = 0; j < matrixSize; j++) {
                            matrix += Math.floor(Math.random() * 100) + " ";
                        }
                        matrix += (i < matrixSize - 1) ? "<br>⎢" : "<br>⎣";
                    }
                    matrix += " det = " + (Math.random() * 1000).toFixed(2);
                    return matrix;
                
                case 3:
                    // Série
                    const seriesVar = getRandomGreekLetter();
                    const seriesLimit = Math.floor(Math.random() * 20) + 10;
                    return `∑<sub>n=1</sub><sup>${seriesLimit}</sup> ${seriesVar}<sub>n</sub> = ${(Math.random() * 10000).toFixed(2)}`;
                
                case 4:
                    // Expressão complexa
                    const terms = Math.floor(Math.random() * 3) + 2;
                    let expr = "";
                    for (let i = 0; i < terms; i++) {
                        const coef = (Math.random() * 100).toFixed(2);
                        const variable = getRandomGreekLetter();
                        const power = Math.floor(Math.random() * 5) + 1;
                        expr += `${coef}${variable}<sup>${power}</sup>`;
                        if (i < terms - 1) {
                            expr += [" + ", " - ", " × ", " ÷ "][Math.floor(Math.random() * 4)];
                        }
                    }
                    expr += ` = ${(Math.random() * 100000).toFixed(4)}`;
                    return expr;
            }
        }
        
        // Função para obter uma letra grega aleatória
        function getRandomGreekLetter() {
            return greekLetters[Math.floor(Math.random() * greekLetters.length)];
        }
        
        // Função para obter um caractere especial aleatório
        function getRandomSpecialChar() {
            return specialChars[Math.floor(Math.random() * specialChars.length)];
        }
        
        // Iniciar a barra de progresso
        setTimeout(() => {
            progressBar.style.width = '100%';
        }, 100);
        
        // Gerar cálculos aleatórios a cada 100ms
        const interval = setInterval(() => {
            calculationArea.innerHTML += generateRandomCalculation() + '<br><br>';
            calculationArea.scrollTop = calculationArea.scrollHeight;
        }, 100);
        
        // Redirecionar para a página de resultado após 15 segundos
        setTimeout(() => {
            clearInterval(interval);
            window.location.href = '/resultado';
        }, 15000);
    </script>
</body>
</html>"""

resultado_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resultado da Análise</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #ffebee;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }
        .container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
            padding: 30px;
            width: 90%;
            max-width: 500px;
            text-align: center;
        }
        h1 {
            color: #e91e63;
            margin-bottom: 20px;
        }
        .result {
            font-size: 24px;
            margin: 30px 0;
            padding: 20px;
            background-color: #f8bbd0;
            border-radius: 10px;
            color: #880e4f;
        }
        .heart {
            color: #e91e63;
            font-size: 30px;
            animation: pulse 1.5s infinite;
        }
        .restart-btn {
            background-color: #e91e63;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
            text-decoration: none;
            display: inline-block;
            margin-top: 20px;
        }
        .restart-btn:hover {
            background-color: #c2185b;
        }
        .confetti {
            position: fixed;
            width: 10px;
            height: 10px;
            background-color: #f48fb1;
            position: absolute;
            top: -10px;
            z-index: -1;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Resultado da Análise</h1>
        <div class="result">
            <span class="heart">❤️</span> 
            Pedro ama mais a Ana 
            <span class="heart">❤️</span>
        </div>
        <p>Nossa análise avançada de compatibilidade revelou este resultado surpreendente!</p>
        <a href="/" class="restart-btn">Fazer Nova Análise</a>
    </div>

    <script>
        // Criar confetes para celebração
        function createConfetti() {
            const confetti = document.createElement('div');
            confetti.classList.add('confetti');
            
            // Cores aleatórias
            const colors = ['#e91e63', '#f48fb1', '#f8bbd0', '#fce4ec', '#880e4f'];
            confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            
            // Posição aleatória
            confetti.style.left = Math.random() * 100 + 'vw';
            
            // Tamanho aleatório
            const size = Math.random() * 8 + 5;
            confetti.style.width = size + 'px';
            confetti.style.height = size + 'px';
            
            // Animação
            confetti.style.animation = `fall ${Math.random() * 3 + 2}s linear`;
            
            document.body.appendChild(confetti);
            
            setTimeout(() => {
                confetti.remove();
            }, 5000);
        }
        
        // Criar confetes a cada 100ms
        setInterval(createConfetti, 100);
        
        // Adicionar animação CSS
        const style = document.createElement('style');
        style.textContent = `
            @keyframes fall {
                to {
                    transform: translateY(100vh) rotate(720deg);
                }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>"""

# Função para criar os templates
def criar_templates():
    with open('templates/index.html', 'w') as f:
        f.write(index_html)
    with open('templates/calculando.html', 'w') as f:
        f.write(calculando_html)
    with open('templates/resultado.html', 'w') as f:
        f.write(resultado_html)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    nome1 = request.form['nome1']
    nome2 = request.form['nome2']
    data1 = request.form['data1']
    data2 = request.form['data2']
    
    # Armazenar os dados na sessão para uso posterior
    return render_template('calculando.html', nome1=nome1, nome2=nome2, data1=data1, data2=data2)

@app.route('/resultado')
def resultado():
    return render_template('resultado.html')

if __name__ == '__main__':
    # Criar os templates antes de iniciar o servidor
    criar_templates()
    app.run(host='0.0.0.0', debug=True)
