# 🏦 Sistema Bancário Python

[![Python](https://img.shields.io/badge/Python-3.13.2-blue.svg)](https://www.python.org/downloads/)
[![MyPy](https://img.shields.io/badge/mypy-checked-blue.svg)](http://mypy-lang.org/)
[![Pytest](https://img.shields.io/badge/pytest-passing-green.svg)](https://pytest.org/)

> Sistema bancário modularizado desenvolvido em Python com gestão de usuários, contas correntes e operações bancárias completas.

## 📋 **Funcionalidades**

### **👥 Gestão de Usuários**

- ✅ **Criar Usuários**: Cadastro com nome, CPF, data de nascimento e endereço
- ✅ **Validação de CPF**: Verificação de unicidade e formato
- ✅ **Listagem**: Visualização de todos os usuários cadastrados

### **🏦 Gestão de Contas**

- ✅ **Criar Contas Correntes**: Vinculadas a usuários existentes
- ✅ **Numeração Sequencial**: Agência fixa "0001" e numeração automática
- ✅ **Múltiplas Contas**: Um usuário pode ter várias contas
- ✅ **Seleção de Conta**: Escolha da conta para operações

### **💰 Operações Bancárias**

- ✅ **Depósitos**: Operações com validação de valores positivos
- ✅ **Saques**: Sistema com múltiplas validações:
  - Limite de R$ 500,00 por saque
  - Máximo 3 saques por dia
  - Verificação de saldo suficiente
- ✅ **Extrato**: Histórico completo com data, hora e saldos

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

O sistema apresenta um menu interativo moderno:

```
🏦 SISTEMA BANCÁRIO - VERSÃO 2.0
============================================================
1️⃣  Criar Usuário
2️⃣  Criar Conta Corrente
3️⃣  Selecionar Conta
4️⃣  Depositar
5️⃣  Sacar
6️⃣  Visualizar Extrato
7️⃣  Listar Usuários
8️⃣  Listar Contas
9️⃣  Sair
============================================================
```

### **Fluxo de Uso Completo**

1. **Criar Usuário**: Nome, CPF, data nascimento e endereço completo
2. **Criar Conta Corrente**: Informar CPF do usuário
3. **Selecionar Conta**: Agência + número da conta
4. **Realizar Operações**: Depósitos, saques e consultas
5. **Visualizar Extrato**: Histórico detalhado com CPF e dados da conta

### **Exemplo Prático**

```
👤 Criar Usuário: João Silva, CPF 123.456.789-01
🏦 Criar Conta: Agência 0001, Conta 1
💰 Depositar: R$ 1.500,00
💸 Sacar: R$ 300,00 (dentro dos limites)
📋 Extrato: Histórico completo com saldos
```

## 🧪 **Testes**

### **Cobertura Completa**

```bash
# Executar todos os testes (49 testes)
pytest -v

# Testes com cobertura de código
pytest --cov=main --cov-report=html

# Verificar tipagem estática
mypy main.py conftest.py test_main.py
```

### **Categorias de Testes**

- ✅ **Testes Unitários**: Cada classe e método isoladamente
- ✅ **Testes de Integração**: Fluxos completos do sistema
- ✅ **Testes Parametrizados**: Múltiplos cenários automatizados
- ✅ **Testes com Fixtures**: Reutilização de objetos de teste
- ✅ **Mocking Completo**: Isolamento de dependências externas

## 🔒 **Regras de Negócio**

### **Usuários**

- CPF único no sistema (não permite duplicatas)
- Todos os campos obrigatórios
- Formatação automática do CPF

### **Contas Correntes**

- Agência fixa: "0001"seu-perfil
- Numeração sequencial automática
- Vinculação obrigatória a usuário existente
- Um usuário pode ter múltiplas contas

### **Operações Financeiras**

- **Depósitos**: Apenas valores positivos
- **Saques**:
  - Limite máximo: R$ 500,00 por operação
  - Limite diário: 3 saques por dia
  - Saldo suficiente obrigatório
- **Precisão**: Valores em centavos (inteiros) para evitar problemas de float

## 🏗️ **Arquitetura Modularizada**

### **Classes Principais**

```python
class Usuario:          # Gestão de clientes
class ContaCorrente:    # Operações bancárias
class SistemaBancario:  # Coordenação geral
```

### **Funções Modulares**

```python
depositar(conta, valor)        # Operação de depósito
sacar(conta, valor)           # Operação de saque
visualizar_historico(conta)   # Exibição de extrato
```

### **Estrutura de Arquivos**

```
santander-python-bank/
├── main.py              # Sistema principal (classes + main)
├── test_main.py         # Testes unitários e integração
├── conftest.py          # Fixtures para testes
├── requirements.txt     # Dependências (pytest, mypy, etc)
├── .python-version      # Versão Python (3.13.2)
├── pytest.ini          # Configuração de testes
└── README.md           # Esta documentação
```

## 💡 **Tecnologias e Boas Práticas**

### **Linguagem e Tipagem**

- **Python 3.13.2**: Versão mais recente
- **Type Hints**: Tipagem completa em todas as funções
- **MyPy**: Verificação estática de tipos

### **Qualidade de Código**

- **Pytest**: Framework de testes robusto
- **Fixtures**: Reutilização de objetos de teste
- **Mocking**: Isolamento de dependências
- **Cobertura**: Testes abrangentes (49 casos)

### **Precisão Financeira**

- **Armazenamento**: Valores em centavos (int)
- **Conversão**: Automática real ↔ centavos
- **Formatação**: Exibição em R$ xxx,xx

## 📊 **Estatísticas do Projeto**

- 🧪 **49 testes** passando
- 📝 **500+ linhas** de código
- 🎯 **100% tipado** com MyPy
- 🏗️ **3 classes** principais
- ⚡ **6 operações** bancárias
- 🔒 **Multiple validações** de segurança

## 👨‍💻 **Autor**

Desenvolvido por **@inacio-dev** durante o bootcamp **Santander - Python**.

**Conecte-se:**

- 🐙 GitHub: [@inacio-dev](https://github.com/inacio-dev)
- 💼 LinkedIn: [Seu LinkedIn](https://linkedin.com/in/inacio-rodrigues-dev)

---

⭐ **Se foi útil, considere dar uma estrela no repositório!**
