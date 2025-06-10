# 🏦 Sistema Bancário Python

[![Python](https://img.shields.io/badge/Python-3.13.2-blue.svg)](https://www.python.org/downloads/)
[![MyPy](https://img.shields.io/badge/mypy-checked-blue.svg)](http://mypy-lang.org/)
[![Pytest](https://img.shields.io/badge/pytest-passing-green.svg)](https://pytest.org/)

> Sistema bancário desenvolvido em Python com operações básicas, tipagem estática e testes unitários.

## 📋 **Funcionalidades**

- ✅ **Criar Contas**: Cadastro de contas bancárias
- ✅ **Depósitos**: Operações de depósito com validação
- ✅ **Saques**: Sistema com validações:
  - Limite de R$ 500,00 por saque
  - Máximo 3 saques por dia
  - Verificação de saldo suficiente
- ✅ **Extrato**: Histórico completo de transações
- ✅ **Múltiplas Contas**: Suporte a várias contas

## 🚀 **Instalação**

### **Pré-requisitos**

- Python 3.13.2

### **1. Clone o Repositório**

```bash
git clone https://github.com/inacio-dev/santander-python-bank.git
cd santander-python-bank
```

### **2. Crie e Ative o Ambiente Virtual**

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### **3. Instale as Dependências**

```bash
pip install -r requirements.txt
```

### **4. Execute o Sistema**

```bash
python main.py
```

## 🎮 **Como Usar**

O sistema apresenta um menu interativo:

```
🏦 SISTEMA BANCÁRIO
==================================================
1️⃣  Criar Conta
2️⃣  Selecionar Conta
3️⃣  Depositar
4️⃣  Sacar
5️⃣  Visualizar Extrato
6️⃣  Listar Contas
7️⃣  Sair
==================================================
```

### **Exemplo de Fluxo**

1. Criar uma nova conta
2. Selecionar a conta criada
3. Realizar depósito (ex: R$ 1.000,00)
4. Realizar saques (respeitando limites)
5. Visualizar extrato completo

## 🧪 **Testes**

```bash
# Executar todos os testes
pytest -v

# Testes com cobertura
pytest --cov=main --cov-report=html

# Verificar tipagem
mypy main.py
```

## 🔒 **Regras de Negócio**

### **Depósitos**

- Apenas valores positivos
- Registro automático no histórico

### **Saques**

- Limite: R$ 500,00 por operação
- Máximo: 3 saques diários
- Saldo suficiente obrigatório

### **Precisão Financeira**

- Valores armazenados em centavos (inteiros)
- Evita problemas de precisão com float

## 🏗️ **Estrutura**

```
santander-python-bank/
├── main.py                    # Sistema principal
├── test_main.py              # Testes unitários
├── conftest.py               # Configurações de teste
├── requirements.txt          # Dependências
├── .python-version          # Versão Python (3.13.2)
└── README.md               # Documentação
```

## 👨‍💻 **Autor**

Desenvolvido durante o bootcamp **Santander - Python**.

---
