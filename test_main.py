import pytest

from main import ContaBancaria, SistemaBancario


class TestExemplosFixtures:
    def test_conta_basica(self, conta_bancaria: ContaBancaria) -> None:
        """Teste usando fixture de conta básica."""
        assert conta_bancaria._numero_conta == "12345-6"
        assert conta_bancaria._titular == "João Silva"
        assert conta_bancaria.get_saldo_centavos() == 0

    def test_conta_com_saldo(self, conta_com_saldo: ContaBancaria) -> None:
        """Teste usando fixture de conta com saldo."""
        assert conta_com_saldo.get_saldo_centavos() == 100000  # R$ 1000,00

        resultado = conta_com_saldo.sacar(500.0)
        assert resultado is True
        assert conta_com_saldo.get_saldo_centavos() == 50000  # R$ 500,00

    def test_sistema_bancario(self, sistema_bancario: SistemaBancario) -> None:
        """Teste usando fixture de sistema bancário."""
        assert len(sistema_bancario._contas) == 0
        assert sistema_bancario.get_conta_atual() is None

    def test_sistema_com_conta(self, sistema_com_conta: SistemaBancario) -> None:
        """Teste usando fixture de sistema com conta."""
        assert len(sistema_com_conta._contas) == 1
        conta_atual = sistema_com_conta.get_conta_atual()
        assert conta_atual is not None
        assert conta_atual._numero_conta == "12345-6"

    def test_limite_saque(self, conta_com_limite_saque: ContaBancaria) -> None:
        """Teste usando fixture de conta com limite de saque."""
        # Tenta sacar acima do limite
        resultado = conta_com_limite_saque.sacar(600.0)
        assert resultado is False

        # Saque dentro do limite
        resultado = conta_com_limite_saque.sacar(500.0)
        assert resultado is True

    def test_multiplas_contas(self, sistema_multiplas_contas: SistemaBancario) -> None:
        """Teste usando fixture de sistema com múltiplas contas."""
        assert len(sistema_multiplas_contas._contas) == 3

        # Testa seleção de diferentes contas
        assert sistema_multiplas_contas.selecionar_conta("11111-1") is True
        assert sistema_multiplas_contas.selecionar_conta("99999-9") is False

    def test_extrato_com_historico(self, conta_para_extrato: ContaBancaria) -> None:
        """Teste usando fixture de conta com histórico."""
        assert len(conta_para_extrato._historico) == 4  # 2 depósitos + 2 saques
        assert conta_para_extrato.get_saldo_centavos() == 120000  # R$ 1200,00

    def test_ambiente_teste(self, ambiente_teste: dict[str, str]) -> None:
        assert ambiente_teste["ambiente"] == "teste"
        assert ambiente_teste["debug"] == "true"

    def test_configuracao_global(self, configuracao_global: dict[str, str]) -> None:
        """Teste usando fixture de escopo de sessão."""
        assert configuracao_global["versao_sistema"] == "1.0.0"
        assert configuracao_global["banco_teste"] == "Banco PyTest"

    def test_dados_modulo(self, dados_modulo: dict[str, int]) -> None:
        """Teste usando fixture de escopo de módulo."""
        assert dados_modulo["limite_saque"] == 50000
        assert dados_modulo["limite_saques_diarios"] == 3


class TestCombinacoesFixtures:
    def test_transferencia_entre_contas(
        self, sistema_multiplas_contas: SistemaBancario, configuracao_global: dict[str, str]
    ) -> None:
        """Simula transferência usando múltiplas fixtures."""
        # Seleciona primeira conta e deposita
        sistema_multiplas_contas.selecionar_conta("11111-1")
        conta1 = sistema_multiplas_contas.get_conta_atual()
        assert conta1 is not None
        conta1.depositar(1000.0)

        # Seleciona segunda conta
        sistema_multiplas_contas.selecionar_conta("22222-2")
        conta2 = sistema_multiplas_contas.get_conta_atual()
        assert conta2 is not None

        # Verifica configuração global
        assert configuracao_global["moeda"] == "BRL"

        # Simula "transferência" (saque + depósito)
        sistema_multiplas_contas.selecionar_conta("11111-1")
        conta1.sacar(500.0)

        sistema_multiplas_contas.selecionar_conta("22222-2")
        conta2.depositar(500.0)

        assert conta1.get_saldo_centavos() == 50000  # R$ 500,00
        assert conta2.get_saldo_centavos() == 50000  # R$ 500,00

    def test_validacao_limites(self, conta_com_saldo: ContaBancaria, dados_modulo: dict[str, int]) -> None:
        """Testa limites usando dados do módulo."""
        limite_centavos = dados_modulo["limite_saque"]
        limite_saques = dados_modulo["limite_saques_diarios"]

        # Testa limite por saque
        valor_acima_limite = (limite_centavos + 1) / 100
        resultado = conta_com_saldo.sacar(valor_acima_limite)
        assert resultado is False

        # Testa limite de saques diários
        for _i in range(limite_saques):
            resultado = conta_com_saldo.sacar(100.0)
            assert resultado is True

        # Quarto saque deve falhar
        resultado = conta_com_saldo.sacar(100.0)
        assert resultado is False


@pytest.fixture(params=[("12345-6", "João Silva"), ("67890-1", "Maria Santos"), ("11111-1", "Pedro Oliveira")])
def conta_parametrizada(request: pytest.FixtureRequest) -> ContaBancaria:
    """Fixture parametrizada que cria contas com diferentes dados."""
    numero, titular = request.param
    return ContaBancaria(numero, titular)


class TestFixtureParametrizada:
    """Testes usando fixture parametrizada."""

    def test_contas_diferentes(self, conta_parametrizada: ContaBancaria) -> None:
        """Teste executado 3 vezes com contas diferentes."""
        assert len(conta_parametrizada._numero_conta) > 0
        assert len(conta_parametrizada._titular) > 0
        assert conta_parametrizada.get_saldo_centavos() == 0
