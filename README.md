# 🏦 Sistema Bancário Python - Versão 3.0 (Classes)

[![Python](https://img.shields.io/badge/Python-3.13.2-blue.svg)](https://www.python.org/downloads/)
[![MyPy](https://img.shields.io/badge/mypy-checked-blue.svg)](http://mypy-lang.org/)
[![Tests](https://img.shields.io/badge/tests-84%20passed-green.svg)](https://pytest.org/)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](https://pytest-cov.readthedocs.io/)

> Sistema bancário orientado a objetos desenvolvido em Python com herança, polimorfismo e classes abstratas.

## 🆕 **Novidades da Versão 3.0**

### **🏗️ Arquitetura Orientada a Objetos**

- ✅ **Classes Abstratas**: Transacao como classe base abstrata
- ✅ **Herança**: Cliente → PessoaFisica, Conta → ContaCorrente
- ✅ **Polimorfismo**: Diferentes tipos de transação (Saque, Deposito)
- ✅ **Encapsulamento**: Propriedades e métodos privados/protegidos
- ✅ **Composição**: Cliente possui Contas, Conta possui Historico

### **📊 Diagrama de Classes UML Implementado**

```
Cliente (base)
├── endereco: str
├── contas: List[Conta]
├── realizar_transacao()
└── adicionar_conta()

PessoaFisica(Cliente)
├── nome: str
├── data_nascimento: str
├── cpf: str
└── get_cpf_formatado()

Conta (base)
├── _saldo_centavos: int
├── _numero: int
├── _agencia: str
├── _cliente: Cliente
├── _historico: Historico
├── sacar()
├── depositar()
└── nova_conta() @classmethod

ContaCorrente(Conta)
├── _limite_centavos: int
├── _limite_saques: int
├── _saques_realizados_hoje: int
└── sacar() @override

Historico
├── _transacoes: List[Transacao]
├── adicionar_transacao()
├── gerar_relatorio()
└── transacoes_do_dia()

Transacao (ABC)
├── valor: float @property @abstractmethod
└── registrar() @abstractmethod

Saque(Transacao)
├── _valor: float
├── data_hora: datetime
└── registrar()

Deposito(Transacao)
├── _valor: float
├── data_hora: datetime
└── registrar()
```

## 🚀 **Instalação e Execução**

### **1. Clone e Configure**

```bash
git clone https://github.com/inacio-dev/santander-python-bank.git
cd santander-python-bank
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### **2. Execute o Sistema**

```bash
python main.py
```

### **3. Verificar Instalação**

```bash
# Verificar tipagem
mypy main.py conftest.py test_main.py

# Executar testes
pytest -v

# Verificar cobertura
pytest --cov=main --cov-report=html
```

## 🎮 **Interface Atualizada**

O sistema apresenta um menu moderno integrado com as classes:

```
🏦 SISTEMA BANCÁRIO - VERSÃO 3.0 (CLASSES)
============================================================
1️⃣  Criar Usuário
2️⃣  Criar Conta Corrente
3️⃣  Depositar
4️⃣  Sacar
5️⃣  Visualizar Extrato
6️⃣  Listar Usuários
7️⃣  Listar Contas
8️⃣  Relatório de Transações
9️⃣  Sair
============================================================
```

## 🔧 **Principais Melhorias Implementadas**

### **🏗️ Padrões de Design Aplicados**

#### **1. Strategy Pattern (Transações)**

```python
# Classe abstrata define a interface
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta: Conta) -> None:
        pass

# Implementações concretas
class Saque(Transacao):
    def registrar(self, conta: Conta) -> None:
        conta.sacar(self.valor)

class Deposito(Transacao):
    def registrar(self, conta: Conta) -> None:
        conta.depositar(self.valor)
```

#### **2. Factory Method (Criação de Contas)**

```python
class Conta:
    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> 'Conta':
        return cls(cliente, numero)

# Uso
conta = ContaCorrente.nova_conta(cliente, 123)
```

#### **3. Composition (Cliente e Contas)**

```python
class Cliente:
    def __init__(self, endereco: str):
        self.contas: List[Conta] = []  # Composição

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        transacao.registrar(conta)
```

### **🔒 Controles de Negócio Aprimorados**

#### **1. Limite de Transações Diárias**

- ✅ **10 transações máximas por dia por cliente**
- ✅ **Validação automática antes de cada operação**
- ✅ **Reset automático a cada novo dia**

#### **2. Histórico Inteligente**

```python
class Historico:
    def gerar_relatorio(self, tipo_transacao: Optional[str] = None) -> str:
        # Filtra por tipo específico ou mostra todas

    def transacoes_do_dia(self) -> List[Transacao]:
        # Retorna apenas transações do dia atual
```

#### **3. Múltiplas Contas por Cliente**

- ✅ **Cliente pode ter várias contas correntes**
- ✅ **Seleção automática ou manual de conta**
- ✅ **Listagem inteligente das contas disponíveis**

## 🧪 **Testes Abrangentes**

### **Cobertura de Testes**

```bash
# Executar todos os testes (84 casos)
pytest test_main.py -v

# Testes com cobertura
pytest --cov=main --cov-report=html

# Testes específicos por classe
pytest test_main.py::TestPessoaFisica -v
pytest test_main.py::TestContaCorrente -v
pytest test_main.py::TestTransacoes -v
```

### **Categorias de Teste Implementadas**

- ✅ **Testes Unitários**: Cada classe isoladamente
- ✅ **Testes de Integração**: Fluxos completos entre classes
- ✅ **Testes Parametrizados**: Múltiplos cenários automatizados
- ✅ **Testes com Fixtures**: Reutilização de objetos
- ✅ **Testes de Herança**: Validação de polimorfismo
- ✅ **Testes de Classes Abstratas**: Implementação correta

## 🎯 **Funcionalidades Avançadas**

### **📊 Relatórios Inteligentes**

#### **1. Relatório por Tipo de Transação**

```python
# Relatório específico
historico.gerar_relatorio("deposito")  # Só depósitos
historico.gerar_relatorio("saque")     # Só saques
historico.gerar_relatorio()            # Todas as transações
```

#### **2. Transações do Dia**

```python
# Filtra automaticamente por data atual
transacoes_hoje = conta.historico.transacoes_do_dia()
print(f"Transações hoje: {len(transacoes_hoje)}")
```

### **⚡ Operações Dinâmicas**

#### **1. Seleção Inteligente de Conta**

```python
def recuperar_conta_cliente(cliente: Cliente) -> Optional[Conta]:
    if len(cliente.contas) == 1:
        return cliente.contas[0]  # Seleção automática
    else:
        # Lista opções para o usuário escolher
        return conta_escolhida
```

#### **2. Validações Robustas**

- ✅ **CPF**: Formato e unicidade
- ✅ **Valores**: Positivos e limites
- ✅ **Datas**: Controle de operações diárias
- ✅ **Contas**: Existência e saldo

## 🏗️ **Arquitetura Modular**

### **Estrutura de Arquivos**

```
sistema-bancario-v3/
├── main.py                        # Sistema principal OOP
├── test_main.py                    # Testes para classes
├── conftest.py                     # Fixtures para testes
├── requirements.txt                # Dependências
├── pytest.ini                     # Configuração de testes
├── pyproject.toml                  # Configuração do projeto
├── .python-version                 # Versão Python
├── .gitignore                      # Arquivos ignorados
└── README.md                       # Esta documentação
```

### **Dependências e Compatibilidade**

```txt
# requirements.txt
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0
```

## 💡 **Exemplos de Uso Avançado**

### **1. Criação Programática**

```python
# Criar cliente e múltiplas contas
cliente = PessoaFisica("João Silva", "01/01/1990", "12345678901", "Rua A, 123")

# Conta corrente principal
conta_principal = ContaCorrente(cliente, limite=1000.0, limite_saques=5)
cliente.adicionar_conta(conta_principal)

# Conta corrente secundária
conta_secundaria = ContaCorrente(cliente, limite=500.0, limite_saques=3)
cliente.adicionar_conta(conta_secundaria)

# Operações usando transações
deposito = Deposito(2000.0)
cliente.realizar_transacao(conta_principal, deposito)

saque = Saque(300.0)
cliente.realizar_transacao(conta_principal, saque)
```

### **2. Relatórios Customizados**

```python
# Análise de movimentação
def analisar_conta(conta: ContaCorrente):
    historico = conta.historico

    # Transações de hoje
    hoje = historico.transacoes_do_dia()

    # Por tipo
    depositos = historico.gerar_relatorio("deposito")
    saques = historico.gerar_relatorio("saque")

    # Estatísticas
    total_depositos = sum(t.valor for t in hoje if isinstance(t, Deposito))
    total_saques = sum(t.valor for t in hoje if isinstance(t, Saque))

    return {
        "saldo": conta.saldo,
        "transacoes_hoje": len(hoje),
        "depositos_hoje": total_depositos,
        "saques_hoje": total_saques
    }
```

## 🔍 **Comparação com Versão Anterior**

| Aspecto              | Versão 2.0 (Dicionários) | Versão 3.0 (Classes)      |
| -------------------- | ------------------------ | ------------------------- |
| **Paradigma**        | Procedural               | Orientado a Objetos       |
| **Estrutura**        | Dicionários e listas     | Classes e herança         |
| **Extensibilidade**  | Limitada                 | Alta (polimorfismo)       |
| **Manutenibilidade** | Média                    | Alta (encapsulamento)     |
| **Testabilidade**    | Boa                      | Excelente (mocking)       |
| **Reutilização**     | Baixa                    | Alta (herança/composição) |
| **Validações**       | Manuais                  | Automáticas (métodos)     |
| **Relatórios**       | Básicos                  | Avançados (filtros)       |

## 🚦 **Regras de Negócio Implementadas**

### **👤 Gestão de Clientes**

- ✅ **CPF único** no sistema
- ✅ **Múltiplas contas** por cliente
- ✅ **Dados obrigatórios** validados
- ✅ **Formatação automática** de CPF

### **🏦 Contas Correntes**

- ✅ **Agência fixa**: "0001"
- ✅ **Numeração sequencial** automática
- ✅ **Limites personalizáveis** por conta
- ✅ **Histórico individual** por conta

### **💰 Transações**

- ✅ **Limite máximo**: R$ 500,00 por saque (configurável)
- ✅ **Limite diário**: 3 saques por dia (configurável)
- ✅ **Limite geral**: 10 transações por dia por cliente
- ✅ **Precisão financeira**: Valores em centavos

### **📊 Relatórios**

- ✅ **Filtros por tipo** de transação
- ✅ **Período específico** (dia atual)
- ✅ **Estatísticas automáticas**
- ✅ **Formatação profissional**

## 🏆 **Benefícios da Arquitetura OOP**

### **1. Manutenibilidade**

- **Responsabilidade única**: Cada classe tem uma função específica
- **Baixo acoplamento**: Classes independentes e intercambiáveis
- **Alta coesão**: Métodos relacionados agrupados logicamente

### **2. Extensibilidade**

- **Novos tipos de conta**: Herdar de `Conta`
- **Novas transações**: Implementar `Transacao`
- **Novos clientes**: Herdar de `Cliente`

### **3. Testabilidade**

- **Isolamento**: Cada classe pode ser testada independentemente
- **Mocking**: Fácil simulação de dependências
- **Fixtures**: Reutilização de objetos de teste

### **4. Reutilização**

- **Herança**: Compartilhamento de código comum
- **Composição**: Combinação flexível de funcionalidades
- **Polimorfismo**: Tratamento uniforme de objetos diferentes

## 📈 **Métricas de Qualidade**

- 🧪 **84 testes** passando com 100% de cobertura
- 📝 **800+ linhas** de código principal
- 🎯 **100% tipado** com MyPy strict mode
- 🏗️ **10 classes** principais implementadas
- ⚡ **8 operações** bancárias disponíveis
- 🔒 **20+ validações** de segurança ativas

## 🔧 **Solução de Problemas**

### **Erro MyPy**

Se encontrar erros de tipo, certifique-se de usar Python 3.13.2:

```bash
python --version  # Deve ser 3.13.2
mypy main.py conftest.py test_main.py
```

### **Testes Falhando**

Verifique se todas as dependências estão instaladas:

```bash
pip install -r requirements.txt
pytest -v  # Deve mostrar 84 testes passando
```

### **Problemas de Importação**

Certifique-se de estar no diretório correto:

```bash
ls -la  # Deve mostrar main.py, test_main.py, conftest.py
```

## 🎓 **Conceitos de POO Demonstrados**

### **Herança**

```python
class Cliente:                    # Classe base
    def realizar_transacao(self): pass

class PessoaFisica(Cliente):      # Herança
    def get_cpf_formatado(self):  # Método específico
        return formatted_cpf
```

### **Polimorfismo**

```python
def processar_transacao(transacao: Transacao):
    transacao.registrar(conta)    # Mesmo método, comportamentos diferentes

# Funciona com Saque, Deposito, ou qualquer Transacao
```

### **Encapsulamento**

```python
class Conta:
    def __init__(self):
        self._saldo_centavos = 0  # Atributo protegido

    @property
    def saldo(self) -> float:     # Acesso controlado
        return self._saldo_centavos / 100
```

### **Abstração**

```python
from abc import ABC, abstractmethod

class Transacao(ABC):             # Classe abstrata
    @abstractmethod
    def registrar(self, conta):   # Método abstrato
        pass
```

## 👨‍💻 **Autor**

Desenvolvido por **@inacio-dev** durante o bootcamp **Santander - Python**.

**Conecte-se:**

- 🐙 GitHub: [@inacio-dev](https://github.com/inacio-dev)
- 💼 LinkedIn: [Inácio Rodrigues](https://linkedin.com/in/inacio-rodrigues-dev)

---

⭐ **Se este projeto foi útil, considere dar uma estrela no repositório!**

🔄 **Versões disponíveis:**

- [v1.0](https://github.com/inacio-dev/santander-python-bank/tree/v1) - Versão procedural básica
- [v2.0](https://github.com/inacio-dev/santander-python-bank/tree/v2) - Sistema modularizado
- **v3.0** - Sistema orientado a objetos (atual)
