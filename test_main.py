from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest

# Import das classes do sistema bancário v3.0
from main import (
    Cliente,
    Conta,
    ContaCorrente,
    Deposito,
    Historico,
    PessoaFisica,
    Saque,
    Transacao,
    filtrar_cliente,
    recuperar_conta_cliente,
    validar_cpf,
)


class TestCliente:
    """Testes para a classe base Cliente."""

    def test_criar_cliente(self) -> None:
        """Testa criação de cliente básico."""
        cliente = Cliente("Rua A, 123 - Centro - SP/SP")

        assert cliente.endereco == "Rua A, 123 - Centro - SP/SP"
        assert cliente.contas == []

    def test_adicionar_conta(self) -> None:
        """Testa adição de conta ao cliente."""
        cliente = Cliente("Rua A, 123")
        pessoa_fisica = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A, 123")
        conta = ContaCorrente(pessoa_fisica)

        cliente.adicionar_conta(conta)

        assert len(cliente.contas) == 1
        assert cliente.contas[0] == conta

    @patch("builtins.print")
    def test_limite_transacoes_diarias(self, mock_print: MagicMock) -> None:
        """Testa limite de 10 transações por dia."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A, 123")
        conta = ContaCorrente(cliente)

        # Simula 11 transações para testar o limite
        for _i in range(11):
            deposito = Deposito(100.0)
            cliente.realizar_transacao(conta, deposito)

        # Verifica se a mensagem de limite foi exibida
        mock_print.assert_any_call("❌ Erro: Limite de 10 transações por dia atingido!")


class TestPessoaFisica:
    """Testes para a classe PessoaFisica."""

    def test_criar_pessoa_fisica(self) -> None:
        """Testa criação de pessoa física."""
        pessoa = PessoaFisica("João Silva", "01/01/1990", "12345678901", "Rua A, 123")

        assert pessoa.nome == "João Silva"
        assert pessoa.data_nascimento == "01/01/1990"
        assert pessoa.cpf == "12345678901"
        assert pessoa.endereco == "Rua A, 123"

    def test_formatar_cpf(self) -> None:
        """Testa formatação do CPF."""
        pessoa = PessoaFisica("João", "01/01/1990", "123.456.789-01", "Rua A, 123")

        # CPF armazenado sem formatação
        assert pessoa.cpf == "12345678901"

        # CPF formatado para exibição
        assert pessoa.get_cpf_formatado() == "123.456.789-01"

    def test_str_pessoa_fisica(self) -> None:
        """Testa representação string da pessoa física."""
        pessoa = PessoaFisica("Maria Santos", "01/01/1990", "12345678901", "Rua B, 456")
        assert str(pessoa) == "Maria Santos - CPF: 123.456.789-01"


class TestConta:
    """Testes para a classe base Conta."""

    def setup_method(self) -> None:
        """Setup executado antes de cada teste."""
        self.cliente = PessoaFisica("João Silva", "01/01/1990", "12345678901", "Rua A, 123")
        self.conta = Conta(self.cliente)

    def test_criar_conta(self) -> None:
        """Testa criação de conta básica."""
        assert self.conta.agencia == "0001"
        assert self.conta.numero >= 1
        assert self.conta.cliente == self.cliente
        assert self.conta.saldo == 0.0

    def test_contador_contas(self) -> None:
        """Testa incremento automático do número da conta."""
        cliente2 = PessoaFisica("Maria", "01/01/1985", "98765432101", "Rua B, 456")
        conta2 = Conta(cliente2)

        assert conta2.numero == self.conta.numero + 1

    @patch("builtins.print")
    def test_depositar_valor_valido(self, mock_print: MagicMock) -> None:
        """Testa depósito com valor válido."""
        resultado = self.conta.depositar(100.50)

        assert resultado is True
        assert self.conta.saldo == 100.50

    @patch("builtins.print")
    def test_depositar_valor_invalido(self, mock_print: MagicMock) -> None:
        """Testa depósito com valor inválido."""
        resultado = self.conta.depositar(-10.0)

        assert resultado is False
        assert self.conta.saldo == 0.0

    @patch("builtins.print")
    def test_sacar_valor_valido(self, mock_print: MagicMock) -> None:
        """Testa saque com valor válido."""
        self.conta.depositar(200.00)
        resultado = self.conta.sacar(50.00)

        assert resultado is True
        assert self.conta.saldo == 150.00

    @patch("builtins.print")
    def test_sacar_saldo_insuficiente(self, mock_print: MagicMock) -> None:
        """Testa saque com saldo insuficiente."""
        resultado = self.conta.sacar(100.0)

        assert resultado is False
        assert self.conta.saldo == 0.0

    def test_metodo_nova_conta(self) -> None:
        """Testa método de classe nova_conta."""
        cliente = PessoaFisica("Pedro", "01/01/1980", "11111111111", "Rua C, 789")
        conta = Conta.nova_conta(cliente, 999)

        assert conta.numero == 999
        assert conta.cliente == cliente

    def test_properties_conta(self) -> None:
        """Testa properties da conta."""
        assert self.conta.saldo == 0.0
        assert self.conta.agencia == "0001"
        assert self.conta.cliente == self.cliente
        assert isinstance(self.conta.historico, Historico)


class TestContaCorrente:
    """Testes para a classe ContaCorrente."""

    def setup_method(self) -> None:
        """Setup executado antes de cada teste."""
        self.cliente = PessoaFisica("João Silva", "01/01/1990", "12345678901", "Rua A, 123")
        self.conta = ContaCorrente(self.cliente)

    def test_criar_conta_corrente(self) -> None:
        """Testa criação de conta corrente."""
        assert self.conta.agencia == "0001"
        assert self.conta.numero >= 1
        assert self.conta.cliente == self.cliente
        assert self.conta.saldo == 0.0

    def test_criar_conta_corrente_com_limites_personalizados(self) -> None:
        """Testa criação de conta corrente com limites personalizados."""
        conta = ContaCorrente(self.cliente, limite=1000.0, limite_saques=5)

        assert conta._limite_centavos == 100000  # R$ 1000 em centavos
        assert conta._limite_saques == 5

    @patch("builtins.print")
    def test_sacar_limite_valor_excedido(self, mock_print: MagicMock) -> None:
        """Testa saque que excede limite por operação."""
        self.conta.depositar(1000.0)
        resultado = self.conta.sacar(600.0)  # Acima do limite de R$ 500

        assert resultado is False
        assert self.conta.saldo == 1000.0

    @patch("builtins.print")
    @patch("main.datetime")
    def test_sacar_limite_diario_excedido(self, mock_datetime: MagicMock, mock_print: MagicMock) -> None:
        """Testa limite de 3 saques diários."""
        mock_datetime.now.return_value.strftime.return_value = "10/06/2025"

        self.conta.depositar(1000.0)

        # Realiza 3 saques válidos
        for _i in range(3):
            resultado = self.conta.sacar(100.0)
            assert resultado is True

        # Quarto saque deve falhar
        resultado = self.conta.sacar(100.0)
        assert resultado is False

    def test_str_conta_corrente(self) -> None:
        """Testa representação string da conta corrente."""
        str_conta = str(self.conta)

        assert "Agência:" in str_conta
        assert "C/C:" in str_conta
        assert "Titular:" in str_conta
        assert self.conta.agencia in str_conta

    @patch("builtins.print")
    def test_reset_contador_saques_novo_dia(self, mock_print: MagicMock) -> None:
        """Testa reset do contador de saques em novo dia."""
        self.conta.depositar(1000.0)

        # Simula saques no primeiro dia
        with patch("main.datetime") as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "10/06/2025"

            for _i in range(3):
                self.conta.sacar(100.0)

            # Quarto saque deve falhar
            assert self.conta.sacar(100.0) is False

        # Simula novo dia
        with patch("main.datetime") as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "11/06/2025"

            # Deve conseguir sacar novamente
            assert self.conta.sacar(100.0) is True


class TestHistorico:
    """Testes para a classe Historico."""

    def setup_method(self) -> None:
        """Setup para testes de histórico."""
        self.historico = Historico()

    def test_criar_historico_vazio(self) -> None:
        """Testa criação de histórico vazio."""
        assert len(self.historico.transacoes) == 0

    def test_adicionar_transacao(self) -> None:
        """Testa adição de transação ao histórico."""
        deposito = Deposito(100.0)
        self.historico.adicionar_transacao(deposito)

        assert len(self.historico.transacoes) == 1
        assert self.historico.transacoes[0] == deposito

    def test_gerar_relatorio_vazio(self) -> None:
        """Testa geração de relatório sem transações."""
        relatorio = self.historico.gerar_relatorio()
        assert "Nenhuma movimentação registrada" in relatorio

    def test_gerar_relatorio_com_transacoes(self) -> None:
        """Testa geração de relatório com transações."""
        deposito = Deposito(100.0)
        saque = Saque(50.0)

        self.historico.adicionar_transacao(deposito)
        self.historico.adicionar_transacao(saque)

        relatorio = self.historico.gerar_relatorio()

        assert "Deposito" in relatorio
        assert "Saque" in relatorio
        assert "100.00" in relatorio
        assert "50.00" in relatorio

    def test_gerar_relatorio_por_tipo(self) -> None:
        """Testa geração de relatório filtrado por tipo."""
        deposito = Deposito(100.0)
        saque = Saque(50.0)

        self.historico.adicionar_transacao(deposito)
        self.historico.adicionar_transacao(saque)

        relatorio_deposito = self.historico.gerar_relatorio("deposito")
        relatorio_saque = self.historico.gerar_relatorio("saque")

        assert "Deposito" in relatorio_deposito
        assert "Saque" not in relatorio_deposito
        assert "Saque" in relatorio_saque
        assert "Deposito" not in relatorio_saque

    def test_gerar_relatorio_tipo_inexistente(self) -> None:
        """Testa geração de relatório para tipo que não existe."""
        deposito = Deposito(100.0)
        self.historico.adicionar_transacao(deposito)

        relatorio = self.historico.gerar_relatorio("transferencia")
        assert "Nenhuma transação do tipo 'transferencia' encontrada" in relatorio

    @patch("main.datetime")
    def test_transacoes_do_dia(self, mock_datetime: MagicMock) -> None:
        """Testa filtro de transações do dia."""
        # Mock da data atual
        mock_date = datetime(2025, 6, 14).date()
        mock_datetime.now.return_value.date.return_value = mock_date

        deposito = Deposito(100.0)
        deposito.data_hora = datetime(2025, 6, 14, 10, 0, 0)

        saque = Saque(50.0)
        saque.data_hora = datetime(2025, 6, 13, 10, 0, 0)  # Dia anterior

        self.historico.adicionar_transacao(deposito)
        self.historico.adicionar_transacao(saque)

        transacoes_hoje = self.historico.transacoes_do_dia()

        assert len(transacoes_hoje) == 1
        assert transacoes_hoje[0] == deposito


class TestTransacoes:
    """Testes para as classes de transação."""

    def setup_method(self) -> None:
        """Setup para testes de transações."""
        self.cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A, 123")
        self.conta = ContaCorrente(self.cliente)

    @patch("builtins.print")
    def test_deposito(self, mock_print: MagicMock) -> None:
        """Testa transação de depósito."""
        deposito = Deposito(100.0)

        assert deposito.valor == 100.0
        assert isinstance(deposito.data_hora, datetime)

        deposito.registrar(self.conta)

        assert self.conta.saldo == 100.0
        assert len(self.conta.historico.transacoes) == 1

    @patch("builtins.print")
    def test_saque(self, mock_print: MagicMock) -> None:
        """Testa transação de saque."""
        # Primeiro faz um depósito
        self.conta.depositar(200.0)

        saque = Saque(50.0)

        assert saque.valor == 50.0
        assert isinstance(saque.data_hora, datetime)

        saque.registrar(self.conta)

        assert self.conta.saldo == 150.0
        assert len(self.conta.historico.transacoes) == 1  # Só o saque é registrado no histórico

    @patch("builtins.print")
    def test_saque_saldo_insuficiente(self, mock_print: MagicMock) -> None:
        """Testa saque com saldo insuficiente."""
        saque = Saque(100.0)
        saque.registrar(self.conta)

        assert self.conta.saldo == 0.0
        assert len(self.conta.historico.transacoes) == 0  # Transação não registrada

    def test_transacao_heranca(self) -> None:
        """Testa que as classes herdam corretamente de Transacao."""
        deposito = Deposito(100.0)
        saque = Saque(50.0)

        # Verifica herança
        assert isinstance(deposito, Transacao)
        assert isinstance(saque, Transacao)

        # Verifica que têm data_hora
        assert hasattr(deposito, "data_hora")
        assert hasattr(saque, "data_hora")

        # Verifica que data_hora é datetime
        assert isinstance(deposito.data_hora, datetime)
        assert isinstance(saque.data_hora, datetime)

    def test_property_valor(self) -> None:
        """Testa property valor da transação."""
        deposito = Deposito(250.75)
        saque = Saque(150.25)

        assert deposito.valor == 250.75
        assert saque.valor == 150.25


class TestFuncoesUtilitarias:
    """Testes para funções utilitárias."""

    def test_validar_cpf_valido(self) -> None:
        """Testa validação de CPF válido."""
        assert validar_cpf("12345678901") is True
        assert validar_cpf("123.456.789-01") is True

    def test_validar_cpf_invalido(self) -> None:
        """Testa validação de CPF inválido."""
        assert validar_cpf("123456789") is False  # Muito curto
        assert validar_cpf("123456789012") is False  # Muito longo
        assert validar_cpf("") is False  # Vazio
        assert validar_cpf("abcdefghijk") is False  # Letras

    def test_filtrar_cliente_existente(self) -> None:
        """Testa filtro de cliente existente."""
        clientes = [
            PessoaFisica("João", "01/01/1990", "12345678901", "Rua A"),
            PessoaFisica("Maria", "01/01/1985", "98765432101", "Rua B"),
        ]

        cliente = filtrar_cliente("123.456.789-01", clientes)
        assert cliente is not None
        assert cliente.nome == "João"

    def test_filtrar_cliente_inexistente(self) -> None:
        """Testa filtro de cliente inexistente."""
        clientes = [PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")]

        cliente = filtrar_cliente("99999999999", clientes)
        assert cliente is None

    def test_filtrar_cliente_lista_vazia(self) -> None:
        """Testa filtro com lista vazia de clientes."""
        clientes: list[PessoaFisica] = []
        cliente = filtrar_cliente("12345678901", clientes)
        assert cliente is None

    @patch("builtins.input", return_value="1")
    @patch("builtins.print")
    def test_recuperar_conta_cliente_uma_conta(self, mock_print: MagicMock, mock_input: MagicMock) -> None:
        """Testa recuperação de conta quando cliente tem apenas uma."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")
        conta = ContaCorrente(cliente)
        cliente.adicionar_conta(conta)

        conta_recuperada = recuperar_conta_cliente(cliente)

        assert conta_recuperada == conta

    @patch("builtins.print")
    def test_recuperar_conta_cliente_sem_conta(self, mock_print: MagicMock) -> None:
        """Testa recuperação de conta quando cliente não tem contas."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")

        conta_recuperada = recuperar_conta_cliente(cliente)

        assert conta_recuperada is None
        mock_print.assert_called_with("\n❌ Cliente não possui conta!")

    @patch("builtins.input", return_value="1")
    @patch("builtins.print")
    def test_recuperar_conta_multiplas_contas(self, mock_print: MagicMock, mock_input: MagicMock) -> None:
        """Testa recuperação quando cliente tem múltiplas contas."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")
        conta1 = ContaCorrente(cliente)
        conta2 = ContaCorrente(cliente)

        cliente.adicionar_conta(conta1)
        cliente.adicionar_conta(conta2)

        conta_recuperada = recuperar_conta_cliente(cliente)

        assert conta_recuperada == conta1  # Primeira conta (escolha 1)

    @patch("builtins.input", return_value="abc")
    @patch("builtins.print")
    def test_recuperar_conta_entrada_invalida(self, mock_print: MagicMock, mock_input: MagicMock) -> None:
        """Testa recuperação com entrada inválida."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")
        conta1 = ContaCorrente(cliente)
        conta2 = ContaCorrente(cliente)

        cliente.adicionar_conta(conta1)
        cliente.adicionar_conta(conta2)

        conta_recuperada = recuperar_conta_cliente(cliente)

        assert conta_recuperada is None
        mock_print.assert_any_call("❌ Digite um número válido!")


class TestIntegracao:
    """Testes de integração do sistema completo."""

    def setup_method(self) -> None:
        """Setup para testes de integração."""
        self.clientes: list[PessoaFisica] = []
        self.contas: list[ContaCorrente] = []

    @patch("builtins.print")
    def test_fluxo_completo_cliente_conta_operacoes(self, mock_print: MagicMock) -> None:
        """Testa fluxo completo: criar cliente, conta e fazer operações."""
        # Criar cliente
        cliente = PessoaFisica("João Silva", "01/01/1990", "12345678901", "Rua A, 123")
        self.clientes.append(cliente)

        # Criar conta
        conta = ContaCorrente(cliente)
        self.contas.append(conta)
        cliente.adicionar_conta(conta)

        # Operações usando transações
        deposito = Deposito(500.0)
        saque = Saque(200.0)

        cliente.realizar_transacao(conta, deposito)
        cliente.realizar_transacao(conta, saque)

        assert conta.saldo == 300.0
        assert len(conta.historico.transacoes) == 2

    @patch("builtins.print")
    def test_multiplos_clientes_e_contas(self, mock_print: MagicMock) -> None:
        """Testa sistema com múltiplos clientes e contas."""
        # Criar clientes
        cliente1 = PessoaFisica("João", "01/01/1990", "11111111111", "Rua A")
        cliente2 = PessoaFisica("Maria", "01/01/1985", "22222222222", "Rua B")

        # Criar contas
        conta1 = ContaCorrente(cliente1)
        conta2 = ContaCorrente(cliente2)

        cliente1.adicionar_conta(conta1)
        cliente2.adicionar_conta(conta2)

        # Verificar que as contas são diferentes
        assert conta1.numero != conta2.numero
        assert conta1.cliente != conta2.cliente

    @patch("builtins.print")
    def test_cliente_multiplas_contas(self, mock_print: MagicMock) -> None:
        """Testa cliente com múltiplas contas."""
        # Criar cliente
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")

        # Criar duas contas para o mesmo cliente
        conta1 = ContaCorrente(cliente)
        conta2 = ContaCorrente(cliente)

        cliente.adicionar_conta(conta1)
        cliente.adicionar_conta(conta2)

        assert len(cliente.contas) == 2
        assert conta1.cliente == cliente
        assert conta2.cliente == cliente
        assert conta1.numero != conta2.numero

    @patch("builtins.print")
    def test_limite_transacoes_integrado(self, mock_print: MagicMock) -> None:
        """Testa limite de transações de forma integrada."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")
        conta = ContaCorrente(cliente)
        cliente.adicionar_conta(conta)

        # Faz 10 depósitos (deve funcionar)
        for _i in range(10):
            deposito = Deposito(100.0)
            cliente.realizar_transacao(conta, deposito)

        assert len(conta.historico.transacoes) == 10

        # 11ª transação deve ser rejeitada
        deposito_extra = Deposito(100.0)
        cliente.realizar_transacao(conta, deposito_extra)

        assert len(conta.historico.transacoes) == 10  # Não aumentou


# Fixture para testes
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
def sistema_com_dados() -> tuple[list[PessoaFisica], list[ContaCorrente]]:
    """Fixture que retorna sistema com dados de teste."""
    clientes: list[PessoaFisica] = []
    contas: list[ContaCorrente] = []

    # Criar clientes
    cliente1 = PessoaFisica("João Silva", "01/01/1990", "11111111111", "Rua A, 123")
    cliente2 = PessoaFisica("Maria Santos", "15/05/1985", "22222222222", "Rua B, 456")

    clientes.extend([cliente1, cliente2])

    # Criar contas
    conta1 = ContaCorrente(cliente1)
    conta2 = ContaCorrente(cliente2)

    cliente1.adicionar_conta(conta1)
    cliente2.adicionar_conta(conta2)

    contas.extend([conta1, conta2])

    return clientes, contas


# Testes usando fixtures
class TestComFixtures:
    """Testes que usam fixtures."""

    def test_cliente_padrao_fixture(self, cliente_padrao: PessoaFisica) -> None:
        """Testa fixture de cliente padrão."""
        assert cliente_padrao.nome == "João Silva"
        assert cliente_padrao.cpf == "12345678901"

    def test_conta_corrente_fixture(self, conta_corrente: ContaCorrente) -> None:
        """Testa fixture de conta corrente."""
        assert conta_corrente.agencia == "0001"
        assert isinstance(conta_corrente.cliente, PessoaFisica)
        assert conta_corrente.cliente.nome == "João Silva"
        assert conta_corrente.saldo == 0.0

    def test_conta_com_saldo_fixture(self, conta_com_saldo: ContaCorrente) -> None:
        """Testa fixture de conta com saldo."""
        assert conta_com_saldo.saldo == 1000.0

    @patch("builtins.print")
    def test_transacao_com_fixture(self, mock_print: MagicMock, conta_com_saldo: ContaCorrente) -> None:
        """Testa transação usando fixture."""
        saque = Saque(200.0)
        saque.registrar(conta_com_saldo)

        assert conta_com_saldo.saldo == 800.0
        assert len(conta_com_saldo.historico.transacoes) == 1

    def test_sistema_com_dados_fixture(self, sistema_com_dados: tuple[list[PessoaFisica], list[ContaCorrente]]) -> None:
        """Testa fixture do sistema com dados."""
        clientes, contas = sistema_com_dados

        assert len(clientes) == 2
        assert len(contas) == 2
        assert clientes[0].nome == "João Silva"
        assert clientes[1].nome == "Maria Santos"


# Testes parametrizados
class TestParametrizados:
    """Testes parametrizados."""

    @pytest.mark.parametrize("valor_deposito", [100.0, 500.0, 1000.0])
    @patch("builtins.print")
    def test_depositos_parametrizados(
        self, mock_print: MagicMock, valor_deposito: float, cliente_padrao: PessoaFisica
    ) -> None:
        """Testa depósitos com valores parametrizados."""
        conta = ContaCorrente(cliente_padrao)
        deposito = Deposito(valor_deposito)

        deposito.registrar(conta)

        assert conta.saldo == valor_deposito

    @pytest.mark.parametrize(
        ("cpf", "esperado"),
        [
            ("12345678901", True),
            ("123.456.789-01", True),
            ("123456789", False),
            ("123456789012", False),
            ("", False),
            ("abcdefghijk", False),
            ("123.456.789-0", False),
        ],
    )
    def test_validacao_cpf_parametrizada(self, cpf: str, esperado: bool) -> None:
        """Testa validação de CPF com parâmetros."""
        resultado = validar_cpf(cpf)
        assert resultado == esperado

    @pytest.mark.parametrize(
        ("valor_saque", "saldo_inicial", "deve_funcionar"),
        [
            (100.0, 500.0, True),  # Saque válido
            (500.0, 1000.0, True),  # Saque no limite
            (600.0, 1000.0, False),  # Acima do limite
            (100.0, 50.0, False),  # Saldo insuficiente
            (0.0, 100.0, False),  # Valor inválido
            (-50.0, 100.0, False),  # Valor negativo
        ],
    )
    @patch("builtins.print")
    def test_saques_parametrizados(
        self,
        mock_print: MagicMock,
        valor_saque: float,
        saldo_inicial: float,
        deve_funcionar: bool,
        cliente_padrao: PessoaFisica,
    ) -> None:
        """Testa saques com diferentes parâmetros."""
        conta = ContaCorrente(cliente_padrao)
        conta.depositar(saldo_inicial)

        resultado = conta.sacar(valor_saque)
        assert resultado == deve_funcionar

    @pytest.mark.parametrize("limite_personalizado", [300.0, 700.0, 1000.0])
    @patch("builtins.print")
    def test_limites_personalizados(
        self, mock_print: MagicMock, limite_personalizado: float, cliente_padrao: PessoaFisica
    ) -> None:
        """Testa contas com limites personalizados."""
        conta = ContaCorrente(cliente_padrao, limite=limite_personalizado)
        conta.depositar(2000.0)

        # Saque dentro do limite deve funcionar
        resultado_dentro = conta.sacar(limite_personalizado)
        assert resultado_dentro is True

        # Saque acima do limite deve falhar
        resultado_acima = conta.sacar(limite_personalizado + 100.0)
        assert resultado_acima is False


# Testes de performance e stress
class TestPerformance:
    """Testes de performance do sistema."""

    @patch("builtins.print")
    def test_muitas_transacoes(self, mock_print: MagicMock) -> None:
        """Testa sistema com muitas transações."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")
        conta = ContaCorrente(cliente)

        # Fazer muitos depósitos pequenos
        for i in range(100):
            deposito = Deposito(10.0)
            if i < 10:  # Só as primeiras 10 são registradas (limite diário)
                cliente.realizar_transacao(conta, deposito)

        assert conta.saldo == 100.0  # 10 depósitos de R$ 10
        assert len(conta.historico.transacoes) == 10

    @patch("builtins.print")
    def test_muitos_clientes(self, mock_print: MagicMock) -> None:
        """Testa sistema com muitos clientes."""
        clientes = []
        contas = []

        # Criar 50 clientes
        for i in range(50):
            cpf = f"{i:011d}"  # CPF sequencial
            cliente = PessoaFisica(f"Cliente {i}", "01/01/1990", cpf, f"Rua {i}")
            conta = ContaCorrente(cliente)

            clientes.append(cliente)
            contas.append(conta)
            cliente.adicionar_conta(conta)

        # Verificar que todos foram criados corretamente
        assert len(clientes) == 50
        assert len(contas) == 50

        # Verificar números únicos das contas
        numeros_contas = [conta.numero for conta in contas]
        assert len(set(numeros_contas)) == 50  # Todos únicos


# Testes de edge cases
class TestEdgeCases:
    """Testes de casos extremos."""

    @patch("builtins.print")
    def test_valor_muito_pequeno(self, mock_print: MagicMock) -> None:
        """Testa operações com valores muito pequenos."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")
        conta = ContaCorrente(cliente)

        # Depósito de 1 centavo
        resultado = conta.depositar(0.01)
        assert resultado is True
        assert conta.saldo == 0.01

    @patch("builtins.print")
    def test_valor_muito_grande(self, mock_print: MagicMock) -> None:
        """Testa operações com valores muito grandes."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")
        conta = ContaCorrente(cliente)

        # Depósito muito grande
        valor_grande = 999999.99
        resultado = conta.depositar(valor_grande)
        assert resultado is True
        assert conta.saldo == valor_grande

    @patch("builtins.print")
    def test_cpf_zeros(self, mock_print: MagicMock) -> None:
        """Testa CPF com zeros."""
        cliente = PessoaFisica("João", "01/01/1990", "00000000000", "Rua A")
        assert cliente.cpf == "00000000000"
        assert cliente.get_cpf_formatado() == "000.000.000-00"

    @patch("builtins.print")
    def test_nome_muito_longo(self, mock_print: MagicMock) -> None:
        """Testa nome muito longo."""
        nome_longo = "João " * 50  # Nome muito longo
        cliente = PessoaFisica(nome_longo, "01/01/1990", "12345678901", "Rua A")
        assert cliente.nome == nome_longo

    @patch("builtins.print")
    def test_endereco_muito_longo(self, mock_print: MagicMock) -> None:
        """Testa endereço muito longo."""
        endereco_longo = "Rua muito longa " * 20
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", endereco_longo)
        assert cliente.endereco == endereco_longo

    @patch("builtins.print")
    def test_transacao_exatamente_no_limite(self, mock_print: MagicMock) -> None:
        """Testa transação exatamente no limite."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")
        conta = ContaCorrente(cliente)
        conta.depositar(1000.0)

        # Saque exatamente no limite
        resultado = conta.sacar(500.0)
        assert resultado is True
        assert conta.saldo == 500.0


# Testes de comportamento específico das classes
class TestComportamentoEspecifico:
    """Testes de comportamentos específicos das classes."""

    @patch("builtins.print")
    def test_historico_preserva_ordem(self, mock_print: MagicMock) -> None:
        """Testa se histórico preserva ordem das transações."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")
        conta = ContaCorrente(cliente)

        # Sequência específica de transações
        deposito1 = Deposito(100.0)
        deposito2 = Deposito(200.0)
        saque1 = Saque(50.0)

        cliente.realizar_transacao(conta, deposito1)
        cliente.realizar_transacao(conta, deposito2)
        cliente.realizar_transacao(conta, saque1)

        transacoes = conta.historico.transacoes
        assert len(transacoes) == 3

        # Primeira transação
        assert isinstance(transacoes[0], Deposito)
        assert transacoes[0].valor == 100.0

        # Segunda transação
        assert isinstance(transacoes[1], Deposito)
        assert transacoes[1].valor == 200.0

        # Terceira transação
        assert isinstance(transacoes[2], Saque)
        assert transacoes[2].valor == 50.0

    @patch("builtins.print")
    def test_conta_nova_conta_com_numero_especifico(self, mock_print: MagicMock) -> None:
        """Testa criação de conta com número específico."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")

        # Criar conta com número específico
        conta_especial = ContaCorrente.nova_conta(cliente, 9999)

        assert conta_especial.numero == 9999
        assert conta_especial.cliente == cliente
        assert conta_especial.agencia == "0001"

    def test_heranca_classes(self) -> None:
        """Testa hierarquia de herança das classes."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")
        conta_corrente = ContaCorrente(cliente)

        # Testa herança
        assert isinstance(cliente, Cliente)
        assert isinstance(conta_corrente, Conta)

        # Testa que métodos da classe base funcionam
        assert hasattr(cliente, "adicionar_conta")
        assert hasattr(conta_corrente, "depositar")
        assert hasattr(conta_corrente, "sacar")

    @patch("builtins.print")
    def test_polimorfismo_transacoes(self, mock_print: MagicMock) -> None:
        """Testa polimorfismo das transações."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")
        conta = ContaCorrente(cliente)
        conta.depositar(1000.0)

        # Lista polimórfica de transações
        transacoes: list[Transacao] = [Deposito(100.0), Saque(50.0), Deposito(200.0)]

        for transacao in transacoes:
            transacao.registrar(conta)  # Polimorfismo em ação

        # Verifica que todas foram registradas corretamente
        historico_transacoes = conta.historico.transacoes
        assert len(historico_transacoes) == 3  # Todas as 3 transações são bem-sucedidas

        # Verifica os tipos e valores das transações
        assert isinstance(historico_transacoes[0], Deposito)
        assert historico_transacoes[0].valor == 100.0

        assert isinstance(historico_transacoes[1], Saque)
        assert historico_transacoes[1].valor == 50.0

        assert isinstance(historico_transacoes[2], Deposito)
        assert historico_transacoes[2].valor == 200.0

        # Verifica saldo final: 1000 + 100 - 50 + 200 = 1250
        assert conta.saldo == 1250.0


# Testes de formatação e exibição
class TestFormatacao:
    """Testes de formatação de dados."""

    def test_formatacao_cpf_diversos_formatos(self) -> None:
        """Testa formatação de CPF com diversos formatos de entrada."""
        formatos_entrada = ["12345678901", "123.456.789-01", "123 456 789 01", "123-456-789-01", "123.456.789.01"]

        for formato in formatos_entrada:
            cliente = PessoaFisica("João", "01/01/1990", formato, "Rua A")
            assert cliente.cpf == "12345678901"
            assert cliente.get_cpf_formatado() == "123.456.789-01"

    @patch("builtins.print")
    def test_formatacao_moeda(self, mock_print: MagicMock) -> None:
        """Testa formatação de valores monetários."""
        cliente = PessoaFisica("João", "01/01/1990", "12345678901", "Rua A")
        conta = ContaCorrente(cliente)

        # Testa diversos valores
        valores_teste = [0.01, 1.00, 10.50, 100.99, 1000.00, 9999.99]

        for valor in valores_teste:
            conta.depositar(valor)
            saldo_formatado = conta.get_saldo_formatado()
            assert saldo_formatado.startswith("R$ ")
            assert "." in saldo_formatado  # Tem separador decimal

            # Reset para próximo teste
            conta._saldo_centavos = 0

    def test_string_representation(self) -> None:
        """Testa representações string das classes."""
        cliente = PessoaFisica("Maria Silva", "01/01/1990", "12345678901", "Rua A")
        conta = ContaCorrente(cliente)

        # Testa __str__ do cliente
        str_cliente = str(cliente)
        assert "Maria Silva" in str_cliente
        assert "123.456.789-01" in str_cliente

        # Testa __str__ da conta
        str_conta = str(conta)
        assert "Agência:" in str_conta
        assert "C/C:" in str_conta
        assert "Titular:" in str_conta


if __name__ == "__main__":
    pytest.main(["-v", "--tb=short", "--color=yes"])
