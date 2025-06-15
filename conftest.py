from collections.abc import Generator

import pytest

from main import Cliente, ContaCorrente, PessoaFisica


@pytest.fixture
def cliente_padrao() -> PessoaFisica:
    """Fixture que retorna um cliente padrão para testes."""
    return PessoaFisica("João Silva", "01/01/1990", "12345678901", "Rua A, 123 - Centro - SP/SP")


@pytest.fixture
def conta_corrente(cliente_padrao: PessoaFisica) -> ContaCorrente:
    """Fixture que retorna uma conta corrente para testes."""
    return ContaCorrente(cliente_padrao)


@pytest.fixture
def conta_com_saldo(cliente_padrao: PessoaFisica) -> ContaCorrente:
    """Fixture que retorna uma conta corrente com saldo."""
    conta = ContaCorrente(cliente_padrao)
    conta.depositar(1000.0)
    return conta


@pytest.fixture
def cliente_base() -> Cliente:
    """Fixture que retorna um cliente base para testes."""
    return Cliente("Rua Base, 123 - Centro - SP/SP")


@pytest.fixture
def conta_com_limite_saque(cliente_padrao: PessoaFisica) -> ContaCorrente:
    """Fixture que retorna uma conta com saldo próximo ao limite de saque."""
    conta = ContaCorrente(cliente_padrao)
    conta.depositar(600.0)  # Acima do limite de R$ 500 por saque
    return conta


@pytest.fixture
def sistema_multiplos_clientes() -> tuple[list[PessoaFisica], list[ContaCorrente]]:
    """Fixture que retorna um sistema com múltiplos clientes e contas."""
    clientes: list[PessoaFisica] = []
    contas: list[ContaCorrente] = []

    # Criar clientes
    cliente1 = PessoaFisica("João Silva", "01/01/1990", "11111111111", "Rua A, 123")
    cliente2 = PessoaFisica("Maria Santos", "15/05/1985", "22222222222", "Rua B, 456")
    cliente3 = PessoaFisica("Pedro Oliveira", "30/12/1980", "33333333333", "Rua C, 789")

    clientes.extend([cliente1, cliente2, cliente3])

    # Criar contas
    conta1 = ContaCorrente(cliente1)
    conta2 = ContaCorrente(cliente2)
    conta3 = ContaCorrente(cliente3)

    cliente1.adicionar_conta(conta1)
    cliente2.adicionar_conta(conta2)
    cliente3.adicionar_conta(conta3)

    contas.extend([conta1, conta2, conta3])

    return clientes, contas


@pytest.fixture
def conta_com_historico(cliente_padrao: PessoaFisica) -> ContaCorrente:
    """Fixture que retorna uma conta com histórico de movimentações."""
    conta = ContaCorrente(cliente_padrao)
    conta.depositar(1000.0)
    conta.sacar(200.0)
    conta.depositar(500.0)
    conta.sacar(100.0)
    return conta


@pytest.fixture
def clientes_diversos() -> list[PessoaFisica]:
    """Fixture que retorna uma lista de clientes para testes."""
    return [
        PessoaFisica("João Silva", "01/01/1990", "11111111111", "Rua A, 123"),
        PessoaFisica("Maria Santos", "15/05/1985", "22222222222", "Rua B, 456"),
        PessoaFisica("Pedro Oliveira", "30/12/1980", "33333333333", "Rua C, 789"),
        PessoaFisica("Ana Costa", "22/08/1995", "44444444444", "Rua D, 101"),
        PessoaFisica("Carlos Lima", "10/03/1988", "55555555555", "Rua E, 202"),
    ]


@pytest.fixture
def sistema_com_multiplas_contas_mesmo_cliente() -> tuple[PessoaFisica, list[ContaCorrente]]:
    """Fixture que retorna cliente com múltiplas contas."""
    cliente = PessoaFisica("João Silva", "01/01/1990", "12345678901", "Rua A, 123")

    # Criar múltiplas contas para o mesmo cliente
    conta1 = ContaCorrente(cliente)
    conta2 = ContaCorrente(cliente)
    conta3 = ContaCorrente(cliente)

    cliente.adicionar_conta(conta1)
    cliente.adicionar_conta(conta2)
    cliente.adicionar_conta(conta3)

    contas = [conta1, conta2, conta3]

    return cliente, contas


# Fixture com setup e teardown usando Generator
@pytest.fixture
def ambiente_teste() -> Generator[dict[str, str]]:
    """Fixture com setup e teardown para ambiente de teste."""
    # Setup
    config_teste = {
        "ambiente": "teste",
        "debug": "true",
        "log_level": "info",
        "agencia_padrao": "0001",
        "limite_transacoes": "10",
    }

    print("\n🔧 Configurando ambiente de teste...")

    yield config_teste  # Fornece o objeto para o teste

    # Teardown
    print("🧹 Limpando ambiente de teste...")


@pytest.fixture(scope="session")
def configuracao_global() -> dict[str, str]:
    """Fixture de escopo de sessão - criada uma vez para todos os testes."""
    return {
        "versao_sistema": "3.0.0",
        "banco_teste": "Banco PyTest v3",
        "moeda": "BRL",
        "agencia_padrao": "0001",
        "tipo_sistema": "orientado_objetos",
    }


@pytest.fixture(scope="module")
def dados_modulo() -> dict[str, int]:
    """Fixture de escopo de módulo - criada uma vez por arquivo de teste."""
    return {
        "limite_saque": 50000,  # R$ 500,00 em centavos
        "limite_saques_diarios": 3,
        "limite_transacoes_diarias": 10,
        "taxa_juros": 5,
    }


# Fixtures parametrizadas
@pytest.fixture(
    params=[
        ("João Silva", "11111111111"),
        ("Maria Santos", "22222222222"),
        ("Pedro Oliveira", "33333333333"),
        ("Ana Costa", "44444444444"),
    ]
)
def cliente_parametrizado(request: pytest.FixtureRequest) -> PessoaFisica:
    """Fixture parametrizada que cria clientes com diferentes dados."""
    nome, cpf = request.param
    return PessoaFisica(nome, "01/01/1990", cpf, f"Endereço de {nome}")


@pytest.fixture(params=[100.0, 500.0, 1000.0, 2500.0])
def valores_deposito(request: pytest.FixtureRequest) -> float:
    """Fixture parametrizada com diferentes valores de depósito."""
    valor: float = request.param
    return valor


@pytest.fixture(params=[50.0, 200.0, 500.0])
def valores_saque(request: pytest.FixtureRequest) -> float:
    """Fixture parametrizada com diferentes valores de saque."""
    valor: float = request.param
    return valor


@pytest.fixture(params=[("0001", 1), ("0001", 2), ("0001", 3)])
def dados_conta(request: pytest.FixtureRequest) -> tuple[str, int]:
    """Fixture parametrizada com dados de conta (agencia, numero)."""
    agencia, numero = request.param
    return agencia, numero


@pytest.fixture(
    params=[
        (300.0, 2),  # Limite R$ 300, 2 saques
        (500.0, 3),  # Limite R$ 500, 3 saques (padrão)
        (800.0, 5),  # Limite R$ 800, 5 saques
        (1000.0, 10),  # Limite R$ 1000, 10 saques
    ]
)
def conta_com_limites_personalizados(request: pytest.FixtureRequest, cliente_padrao: PessoaFisica) -> ContaCorrente:
    """Fixture parametrizada com contas com diferentes limites."""
    limite, limite_saques = request.param
    return ContaCorrente(cliente_padrao, limite=limite, limite_saques=limite_saques)


# Fixtures para casos específicos
@pytest.fixture
def conta_zerada(cliente_padrao: PessoaFisica) -> ContaCorrente:
    """Fixture que retorna uma conta corrente sem saldo."""
    return ContaCorrente(cliente_padrao)


@pytest.fixture
def conta_com_saldo_limite(cliente_padrao: PessoaFisica) -> ContaCorrente:
    """Fixture que retorna uma conta com saldo exatamente no limite de saque."""
    conta = ContaCorrente(cliente_padrao)
    conta.depositar(500.0)  # Exatamente o limite de saque
    return conta


@pytest.fixture
def conta_com_muito_saldo(cliente_padrao: PessoaFisica) -> ContaCorrente:
    """Fixture que retorna uma conta com muito saldo."""
    conta = ContaCorrente(cliente_padrao)
    conta.depositar(10000.0)  # R$ 10.000,00
    return conta


# Fixtures para testes de integração
@pytest.fixture
def sistema_bancario_completo() -> tuple[list[PessoaFisica], list[ContaCorrente]]:
    """Fixture que retorna um sistema bancário completo para testes de integração."""
    clientes: list[PessoaFisica] = []
    contas: list[ContaCorrente] = []

    # Dados de teste mais realistas
    dados_clientes = [
        ("João Silva Santos", "01/01/1985", "12345678901", "Rua das Flores, 123 - Centro - São Paulo/SP"),
        ("Maria Oliveira Costa", "15/05/1990", "98765432101", "Av. Paulista, 456 - Bela Vista - São Paulo/SP"),
        ("Pedro Santos Lima", "22/12/1975", "11122233344", "Rua Augusta, 789 - Consolação - São Paulo/SP"),
        ("Ana Paula Silva", "30/08/1988", "55566677788", "Av. Faria Lima, 321 - Itaim Bibi - São Paulo/SP"),
        ("Carlos Eduardo Souza", "10/03/1992", "99988877766", "Rua Oscar Freire, 654 - Jardins - São Paulo/SP"),
    ]

    for nome, data_nasc, cpf, endereco in dados_clientes:
        # Criar cliente
        cliente = PessoaFisica(nome, data_nasc, cpf, endereco)
        clientes.append(cliente)

        # Criar conta para o cliente
        conta = ContaCorrente(cliente)
        contas.append(conta)
        cliente.adicionar_conta(conta)

        # Adicionar algum saldo inicial variado
        saldos_iniciais = [1000.0, 2500.0, 500.0, 3000.0, 1500.0]
        conta.depositar(saldos_iniciais[len(clientes) - 1])

    return clientes, contas


# Fixtures para testes de performance
@pytest.fixture
def muitos_clientes() -> list[PessoaFisica]:
    """Fixture que cria muitos clientes para testes de performance."""
    clientes = []

    for i in range(100):
        cpf = f"{i:011d}"  # CPF sequencial com zeros à esquerda
        nome = f"Cliente Teste {i:03d}"
        endereco = f"Rua Teste {i}, {i*10} - Bairro {i%10} - Cidade/SP"

        cliente = PessoaFisica(nome, "01/01/1990", cpf, endereco)
        clientes.append(cliente)

    return clientes


# Fixtures para casos de erro
@pytest.fixture
def cliente_sem_contas(cliente_padrao: PessoaFisica) -> PessoaFisica:
    """Fixture que retorna um cliente sem contas."""
    # Garantir que não tem contas
    cliente_padrao.contas.clear()
    return cliente_padrao


# Configuração para marcadores de teste
def pytest_configure(config: pytest.Config) -> None:
    """Configuração de marcadores customizados para pytest."""
    config.addinivalue_line("markers", "slow: marca testes como lentos")
    config.addinivalue_line("markers", "integration: marca testes de integração")
    config.addinivalue_line("markers", "unit: marca testes unitários")
    config.addinivalue_line("markers", "performance: marca testes de performance")
    config.addinivalue_line("markers", "edge_case: marca testes de casos extremos")
