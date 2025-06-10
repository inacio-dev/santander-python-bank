from collections.abc import Generator

import pytest

from main import ContaBancaria, SistemaBancario


@pytest.fixture
def conta_bancaria() -> ContaBancaria:
    """Fixture que retorna uma conta bancária para testes."""
    return ContaBancaria("12345-6", "João Silva")


@pytest.fixture
def conta_com_saldo() -> ContaBancaria:
    """Fixture que retorna uma conta bancária com saldo."""
    conta = ContaBancaria("12345-6", "João Silva")
    conta.depositar(1000.0)
    return conta


@pytest.fixture
def sistema_bancario() -> SistemaBancario:
    """Fixture que retorna um sistema bancário."""
    return SistemaBancario()


@pytest.fixture
def sistema_com_conta() -> SistemaBancario:
    """Fixture que retorna um sistema bancário com uma conta."""
    sistema = SistemaBancario()
    sistema.criar_conta("12345-6", "João Silva")
    sistema.selecionar_conta("12345-6")
    return sistema


@pytest.fixture
def conta_com_limite_saque() -> ContaBancaria:
    """Fixture que retorna uma conta com saldo próximo ao limite de saque."""
    conta = ContaBancaria("99999-9", "Cliente Limite")
    conta.depositar(600.0)  # Acima do limite de R$ 500 por saque
    return conta


@pytest.fixture
def sistema_multiplas_contas() -> SistemaBancario:
    """Fixture que retorna um sistema com múltiplas contas cadastradas."""
    sistema = SistemaBancario()
    sistema.criar_conta("11111-1", "Cliente A")
    sistema.criar_conta("22222-2", "Cliente B")
    sistema.criar_conta("33333-3", "Cliente C")
    return sistema


@pytest.fixture
def conta_para_extrato() -> ContaBancaria:
    """Fixture que retorna uma conta com histórico de movimentações."""
    conta = ContaBancaria("77777-7", "Cliente Histórico")
    conta.depositar(1000.0)
    conta.sacar(200.0)
    conta.depositar(500.0)
    conta.sacar(100.0)
    return conta


@pytest.fixture
def ambiente_teste() -> Generator[dict[str, str]]:
    """Fixture com setup e teardown para ambiente de teste."""
    config_teste = {"ambiente": "teste", "debug": "true", "log_level": "info"}

    print("\n🔧 Configurando ambiente de teste...")

    yield config_teste
    print("🧹 Limpando ambiente de teste...")


@pytest.fixture(scope="session")
def configuracao_global() -> dict[str, str]:
    """Fixture de escopo de sessão - criada uma vez para todos os testes."""
    return {"versao_sistema": "1.0.0", "banco_teste": "Banco PyTest", "moeda": "BRL"}


@pytest.fixture(scope="module")
def dados_modulo() -> dict[str, int]:
    """Fixture de escopo de módulo - criada uma vez por arquivo de teste."""
    return {"limite_saque": 50000, "limite_saques_diarios": 3, "taxa_juros": 5}  # R$ 500,00 em centavos
