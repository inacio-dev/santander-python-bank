from collections.abc import Generator

import pytest

from main import ContaCorrente, SistemaBancario, Usuario


@pytest.fixture
def usuario_padrao() -> Usuario:
    """Fixture que retorna um usuário padrão para testes."""
    return Usuario("João Silva", "01/01/1990", "12345678901", "Rua A, 123 - Centro - SP/SP")


@pytest.fixture
def conta_corrente(usuario_padrao: Usuario) -> ContaCorrente:
    """Fixture que retorna uma conta corrente para testes."""
    return ContaCorrente(usuario_padrao)


@pytest.fixture
def conta_com_saldo(usuario_padrao: Usuario) -> ContaCorrente:
    """Fixture que retorna uma conta corrente com saldo."""
    conta = ContaCorrente(usuario_padrao)
    conta.depositar(1000.0)
    return conta


@pytest.fixture
def sistema_bancario() -> SistemaBancario:
    """Fixture que retorna um sistema bancário limpo."""
    return SistemaBancario()


@pytest.fixture
def sistema_com_usuario_e_conta() -> SistemaBancario:
    """Fixture que retorna um sistema com usuário e conta configurados."""
    sistema = SistemaBancario()
    sistema.criar_usuario("João Silva", "01/01/1990", "12345678901", "Rua A, 123")
    sistema.criar_conta_corrente("12345678901")

    # Seleciona a conta usando o número real da conta criada
    if sistema._contas:
        numero_conta = sistema._contas[0].numero_conta
        sistema.selecionar_conta("0001", numero_conta)

    return sistema


@pytest.fixture
def conta_com_limite_saque(usuario_padrao: Usuario) -> ContaCorrente:
    """Fixture que retorna uma conta com saldo próximo ao limite de saque."""
    conta = ContaCorrente(usuario_padrao)
    conta.depositar(600.0)  # Acima do limite de R$ 500 por saque
    return conta


@pytest.fixture
def sistema_multiplos_usuarios() -> SistemaBancario:
    """Fixture que retorna um sistema com múltiplos usuários e contas."""
    sistema = SistemaBancario()

    # Criar usuários
    sistema.criar_usuario("João Silva", "01/01/1990", "11111111111", "Rua A, 123")
    sistema.criar_usuario("Maria Santos", "15/05/1985", "22222222222", "Rua B, 456")
    sistema.criar_usuario("Pedro Oliveira", "30/12/1980", "33333333333", "Rua C, 789")

    # Criar contas
    sistema.criar_conta_corrente("11111111111")
    sistema.criar_conta_corrente("22222222222")
    sistema.criar_conta_corrente("33333333333")

    return sistema


@pytest.fixture
def conta_com_historico(usuario_padrao: Usuario) -> ContaCorrente:
    """Fixture que retorna uma conta com histórico de movimentações."""
    conta = ContaCorrente(usuario_padrao)
    conta.depositar(1000.0)
    conta.sacar(200.0)
    conta.depositar(500.0)
    conta.sacar(100.0)
    return conta


@pytest.fixture
def usuarios_diversos() -> list[Usuario]:
    """Fixture que retorna uma lista de usuários para testes."""
    return [
        Usuario("João Silva", "01/01/1990", "11111111111", "Rua A, 123"),
        Usuario("Maria Santos", "15/05/1985", "22222222222", "Rua B, 456"),
        Usuario("Pedro Oliveira", "30/12/1980", "33333333333", "Rua C, 789"),
    ]


@pytest.fixture
def sistema_com_multiplas_contas_mesmo_usuario() -> SistemaBancario:
    """Fixture que retorna sistema onde um usuário tem múltiplas contas."""
    sistema = SistemaBancario()

    # Criar usuário
    sistema.criar_usuario("João Silva", "01/01/1990", "12345678901", "Rua A, 123")

    # Criar múltiplas contas para o mesmo usuário
    sistema.criar_conta_corrente("12345678901")  # Conta 1
    sistema.criar_conta_corrente("12345678901")  # Conta 2
    sistema.criar_conta_corrente("12345678901")  # Conta 3

    return sistema


# Fixture com setup e teardown usando Generator
@pytest.fixture
def ambiente_teste() -> Generator[dict[str, str]]:
    """Fixture com setup e teardown para ambiente de teste."""
    # Setup
    config_teste = {"ambiente": "teste", "debug": "true", "log_level": "info", "agencia_padrao": "0001"}

    print("\n🔧 Configurando ambiente de teste...")

    yield config_teste  # Fornece o objeto para o teste

    # Teardown
    print("🧹 Limpando ambiente de teste...")


@pytest.fixture(scope="session")
def configuracao_global() -> dict[str, str]:
    """Fixture de escopo de sessão - criada uma vez para todos os testes."""
    return {"versao_sistema": "2.0.0", "banco_teste": "Banco PyTest", "moeda": "BRL", "agencia_padrao": "0001"}


@pytest.fixture(scope="module")
def dados_modulo() -> dict[str, int]:
    """Fixture de escopo de módulo - criada uma vez por arquivo de teste."""
    return {"limite_saque": 50000, "limite_saques_diarios": 3, "taxa_juros": 5}  # R$ 500,00 em centavos


# Fixtures parametrizadas
@pytest.fixture(
    params=[("João Silva", "11111111111"), ("Maria Santos", "22222222222"), ("Pedro Oliveira", "33333333333")]
)
def usuario_parametrizado(request: pytest.FixtureRequest) -> Usuario:
    """Fixture parametrizada que cria usuários com diferentes dados."""
    nome, cpf = request.param
    return Usuario(nome, "01/01/1990", cpf, f"Endereço de {nome}")


@pytest.fixture(params=[100.0, 500.0, 1000.0])
def valores_deposito(request: pytest.FixtureRequest) -> float:
    """Fixture parametrizada com diferentes valores de depósito."""
    valor: float = request.param
    return valor


@pytest.fixture(params=[("0001", 1), ("0001", 2), ("0001", 3)])
def dados_conta(request: pytest.FixtureRequest) -> tuple[str, int]:
    """Fixture parametrizada com dados de conta (agencia, numero)."""
    agencia, numero = request.param
    return agencia, numero
