from unittest.mock import MagicMock, patch

from main import ContaCorrente, SistemaBancario, Usuario, depositar, sacar, visualizar_historico


class TestUsuario:
    """Testes para a classe Usuario."""

    def test_criar_usuario(self) -> None:
        """Testa criação de usuário."""
        usuario = Usuario("João Silva", "01/01/1990", "12345678901", "Rua A, 123 - Centro - SP/SP")

        assert usuario.nome == "João Silva"
        assert usuario.data_nascimento == "01/01/1990"
        assert usuario.cpf == "12345678901"
        assert usuario.endereco == "Rua A, 123 - Centro - SP/SP"

    def test_formatar_cpf(self) -> None:
        """Testa formatação do CPF."""
        usuario = Usuario("João", "01/01/1990", "123.456.789-01", "Rua A, 123")

        # CPF armazenado sem formatação
        assert usuario.cpf == "12345678901"

        # CPF formatado para exibição
        assert usuario.get_cpf_formatado() == "123.456.789-01"

    def test_str_usuario(self) -> None:
        """Testa representação string do usuário."""
        usuario = Usuario("Maria Santos", "01/01/1990", "12345678901", "Rua B, 456")
        assert str(usuario) == "Maria Santos - CPF: 123.456.789-01"


class TestContaCorrente:
    """Testes para a classe ContaCorrente."""

    def setup_method(self) -> None:
        """Setup executado antes de cada teste."""
        self.usuario = Usuario("João Silva", "01/01/1990", "12345678901", "Rua A, 123")
        self.conta = ContaCorrente(self.usuario)

    def test_criar_conta_corrente(self) -> None:
        """Testa criação de conta corrente."""
        assert self.conta.agencia == "0001"
        assert self.conta.numero_conta >= 1  # Pode variar dependendo da ordem dos testes
        assert self.conta.usuario == self.usuario
        assert self.conta._saldo_centavos == 0

    def test_contador_contas(self) -> None:
        """Testa incremento automático do número da conta."""
        usuario2 = Usuario("Maria", "01/01/1985", "98765432101", "Rua B, 456")
        conta2 = ContaCorrente(usuario2)

        assert conta2.numero_conta == self.conta.numero_conta + 1

    @patch("builtins.print")
    def test_depositar_valor_valido(self, mock_print: MagicMock) -> None:
        """Testa depósito com valor válido."""
        resultado = self.conta.depositar(100.50)

        assert resultado is True
        assert self.conta._saldo_centavos == 10050
        assert len(self.conta._historico) == 1

        # Verifica histórico
        operacao = self.conta._historico[0]
        assert operacao["tipo"] == "DEPÓSITO"
        assert operacao["valor"] == "R$ 100.50"

    @patch("builtins.print")
    def test_depositar_valor_invalido(self, mock_print: MagicMock) -> None:
        """Testa depósito com valor inválido."""
        resultado = self.conta.depositar(-10.0)

        assert resultado is False
        assert self.conta._saldo_centavos == 0
        assert len(self.conta._historico) == 0

    @patch("builtins.print")
    def test_sacar_valor_valido(self, mock_print: MagicMock) -> None:
        """Testa saque com valor válido."""
        self.conta.depositar(200.00)
        resultado = self.conta.sacar(50.00)

        assert resultado is True
        assert self.conta._saldo_centavos == 15000  # 200 - 50 = 150
        assert len(self.conta._historico) == 2

    @patch("builtins.print")
    def test_sacar_saldo_insuficiente(self, mock_print: MagicMock) -> None:
        """Testa saque com saldo insuficiente."""
        resultado = self.conta.sacar(100.0)

        assert resultado is False
        assert self.conta._saldo_centavos == 0

    @patch("builtins.print")
    def test_sacar_limite_valor_excedido(self, mock_print: MagicMock) -> None:
        """Testa saque que excede limite por operação."""
        self.conta.depositar(1000.0)
        resultado = self.conta.sacar(600.0)  # Acima do limite de R$ 500

        assert resultado is False
        assert self.conta._saldo_centavos == 100000

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

    @patch("builtins.print")
    def test_visualizar_extrato(self, mock_print: MagicMock) -> None:
        """Testa visualização do extrato."""
        self.conta.depositar(100.0)
        self.conta.sacar(50.0)
        self.conta.visualizar_extrato()

        calls = [call.args[0] for call in mock_print.call_args_list]
        assert any("📋 EXTRATO BANCÁRIO" in call for call in calls)
        assert any("João Silva" in call for call in calls)

    def test_get_info(self) -> None:
        """Testa obtenção das informações da conta."""
        info = self.conta.get_info()

        assert info["titular"] == "João Silva"
        assert info["cpf"] == "123.456.789-01"
        assert info["agencia"] == "0001"
        assert info["conta"] == str(self.conta.numero_conta)
        assert info["saldo"] == "R$ 0.00"


class TestSistemaBancario:
    """Testes para a classe SistemaBancario."""

    def setup_method(self) -> None:
        """Setup executado antes de cada teste."""
        self.sistema = SistemaBancario()

    @patch("builtins.print")
    def test_criar_usuario_sucesso(self, mock_print: MagicMock) -> None:
        """Testa criação de usuário com sucesso."""
        resultado = self.sistema.criar_usuario("João Silva", "01/01/1990", "12345678901", "Rua A, 123")

        assert resultado is True
        assert len(self.sistema._usuarios) == 1
        assert self.sistema._usuarios[0].nome == "João Silva"

    @patch("builtins.print")
    def test_criar_usuario_cpf_duplicado(self, mock_print: MagicMock) -> None:
        """Testa criação de usuário com CPF duplicado."""
        self.sistema.criar_usuario("João", "01/01/1990", "12345678901", "Rua A")
        resultado = self.sistema.criar_usuario("Maria", "01/01/1985", "12345678901", "Rua B")

        assert resultado is False
        assert len(self.sistema._usuarios) == 1

    @patch("builtins.print")
    def test_criar_conta_corrente_sucesso(self, mock_print: MagicMock) -> None:
        """Testa criação de conta corrente com sucesso."""
        self.sistema.criar_usuario("João", "01/01/1990", "12345678901", "Rua A")
        resultado = self.sistema.criar_conta_corrente("12345678901")

        assert resultado is True
        assert len(self.sistema._contas) == 1
        assert self.sistema._contas[0].usuario.nome == "João"

    @patch("builtins.print")
    def test_criar_conta_usuario_inexistente(self, mock_print: MagicMock) -> None:
        """Testa criação de conta para usuário inexistente."""
        resultado = self.sistema.criar_conta_corrente("99999999999")

        assert resultado is False
        assert len(self.sistema._contas) == 0

    @patch("builtins.print")
    def test_selecionar_conta_existente(self, mock_print: MagicMock) -> None:
        """Testa seleção de conta existente."""
        self.sistema.criar_usuario("João", "01/01/1990", "12345678901", "Rua A")
        self.sistema.criar_conta_corrente("12345678901")

        # Pega o número da conta criada
        numero_conta = self.sistema._contas[0].numero_conta
        resultado = self.sistema.selecionar_conta("0001", numero_conta)

        assert resultado is True
        assert self.sistema._conta_atual is not None
        assert self.sistema._conta_atual.numero_conta == numero_conta

    @patch("builtins.print")
    def test_selecionar_conta_inexistente(self, mock_print: MagicMock) -> None:
        """Testa seleção de conta inexistente."""
        resultado = self.sistema.selecionar_conta("0001", 999)

        assert resultado is False
        assert self.sistema._conta_atual is None

    @patch("builtins.print")
    def test_listar_usuarios_vazio(self, mock_print: MagicMock) -> None:
        """Testa listagem quando não há usuários."""
        self.sistema.listar_usuarios()
        mock_print.assert_called_with("📝 Nenhum usuário cadastrado no sistema.")

    @patch("builtins.print")
    def test_listar_contas_vazio(self, mock_print: MagicMock) -> None:
        """Testa listagem quando não há contas."""
        self.sistema.listar_contas()
        mock_print.assert_called_with("📝 Nenhuma conta cadastrada no sistema.")

    def test_buscar_usuario_por_cpf(self) -> None:
        """Testa busca de usuário por CPF."""
        self.sistema.criar_usuario("João", "01/01/1990", "12345678901", "Rua A")

        # Busca com CPF formatado
        usuario = self.sistema._buscar_usuario_por_cpf("123.456.789-01")
        assert usuario is not None
        assert usuario.nome == "João"

        # Busca com CPF inexistente
        usuario_inexistente = self.sistema._buscar_usuario_por_cpf("99999999999")
        assert usuario_inexistente is None


class TestFuncoesModularizadas:
    """Testes para as funções modularizadas."""

    def setup_method(self) -> None:
        """Setup para testes de funções."""
        usuario = Usuario("João", "01/01/1990", "12345678901", "Rua A")
        self.conta = ContaCorrente(usuario)

    @patch("builtins.print")
    def test_funcao_depositar(self, mock_print: MagicMock) -> None:
        """Testa função depositar modularizada."""
        resultado = depositar(self.conta, 100.0)

        assert resultado is True
        assert self.conta._saldo_centavos == 10000

    @patch("builtins.print")
    def test_funcao_sacar(self, mock_print: MagicMock) -> None:
        """Testa função sacar modularizada."""
        self.conta.depositar(200.0)
        resultado = sacar(self.conta, 100.0)

        assert resultado is True
        assert self.conta._saldo_centavos == 10000

    @patch("builtins.print")
    def test_funcao_visualizar_historico(self, mock_print: MagicMock) -> None:
        """Testa função visualizar_historico modularizada."""
        self.conta.depositar(100.0)
        visualizar_historico(self.conta)

        calls = [call.args[0] for call in mock_print.call_args_list]
        assert any("📋 EXTRATO BANCÁRIO" in call for call in calls)


class TestIntegracao:
    """Testes de integração do sistema completo."""

    def setup_method(self) -> None:
        """Setup para testes de integração."""
        self.sistema = SistemaBancario()

    @patch("builtins.print")
    def test_fluxo_completo_usuario_conta_operacoes(self, mock_print: MagicMock) -> None:
        """Testa fluxo completo: criar usuário, conta e fazer operações."""
        # Criar usuário
        assert self.sistema.criar_usuario("João", "01/01/1990", "12345678901", "Rua A") is True

        # Criar conta
        assert self.sistema.criar_conta_corrente("12345678901") is True

        # Selecionar conta
        numero_conta = self.sistema._contas[0].numero_conta
        assert self.sistema.selecionar_conta("0001", numero_conta) is True

        # Operações
        conta = self.sistema.get_conta_atual()
        assert conta is not None

        assert depositar(conta, 500.0) is True
        assert sacar(conta, 200.0) is True
        assert conta._saldo_centavos == 30000  # R$ 300,00

    @patch("builtins.print")
    def test_multiplos_usuarios_e_contas(self, mock_print: MagicMock) -> None:
        """Testa sistema com múltiplos usuários e contas."""
        # Criar usuários
        self.sistema.criar_usuario("João", "01/01/1990", "11111111111", "Rua A")
        self.sistema.criar_usuario("Maria", "01/01/1985", "22222222222", "Rua B")

        # Criar contas
        self.sistema.criar_conta_corrente("11111111111")
        self.sistema.criar_conta_corrente("22222222222")

        assert len(self.sistema._usuarios) == 2
        assert len(self.sistema._contas) == 2

        # Verificar que as contas são diferentes
        assert self.sistema._contas[0].numero_conta != self.sistema._contas[1].numero_conta

    @patch("builtins.print")
    def test_usuario_multiplas_contas(self, mock_print: MagicMock) -> None:
        """Testa usuário com múltiplas contas."""
        # Criar usuário
        self.sistema.criar_usuario("João", "01/01/1990", "12345678901", "Rua A")

        # Criar duas contas para o mesmo usuário
        self.sistema.criar_conta_corrente("12345678901")
        self.sistema.criar_conta_corrente("12345678901")

        assert len(self.sistema._contas) == 2
        assert self.sistema._contas[0].usuario.cpf == "12345678901"
        assert self.sistema._contas[1].usuario.cpf == "12345678901"


class TestValidacoes:
    """Testes específicos de validações."""

    def test_validar_cpf_valido(self) -> None:
        """Testa validação de CPF válido."""
        from main import validar_cpf

        assert validar_cpf("12345678901") is True
        assert validar_cpf("123.456.789-01") is True

    def test_validar_cpf_invalido(self) -> None:
        """Testa validação de CPF inválido."""
        from main import validar_cpf

        assert validar_cpf("123456789") is False  # Muito curto
        assert validar_cpf("123456789012") is False  # Muito longo
        assert validar_cpf("") is False  # Vazio

    def test_obter_valor_monetario_valido(self) -> None:
        """Testa obtenção de valor monetário válido."""
        from main import obter_valor_monetario

        with patch("builtins.input", return_value="150.50"):
            resultado = obter_valor_monetario("Digite valor: ")
            assert resultado == 150.50

    @patch("builtins.print")
    def test_obter_valor_monetario_invalido(self, mock_print: MagicMock) -> None:
        """Testa obtenção de valor monetário inválido."""
        from main import obter_valor_monetario

        with patch("builtins.input", return_value="abc"):
            resultado = obter_valor_monetario("Digite valor: ")
            assert resultado is None


# Testes usando fixtures
class TestComFixtures:
    """Testes que usam fixtures do conftest.py."""

    def test_usuario_padrao(self, usuario_padrao: Usuario) -> None:
        """Testa fixture de usuário padrão."""
        assert usuario_padrao.nome == "João Silva"
        assert usuario_padrao.cpf == "12345678901"

    def test_conta_corrente_fixture(self, conta_corrente: ContaCorrente) -> None:
        """Testa fixture de conta corrente."""
        assert conta_corrente.agencia == "0001"
        assert conta_corrente.usuario.nome == "João Silva"
        assert conta_corrente._saldo_centavos == 0

    def test_conta_com_saldo_fixture(self, conta_com_saldo: ContaCorrente) -> None:
        """Testa fixture de conta com saldo."""
        assert conta_com_saldo._saldo_centavos == 100000  # R$ 1000,00

    def test_sistema_bancario_fixture(self, sistema_bancario: SistemaBancario) -> None:
        """Testa fixture de sistema bancário."""
        assert len(sistema_bancario._usuarios) == 0
        assert len(sistema_bancario._contas) == 0

    def test_sistema_com_usuario_e_conta_fixture(self, sistema_com_usuario_e_conta: SistemaBancario) -> None:
        """Testa fixture de sistema com usuário e conta."""
        assert len(sistema_com_usuario_e_conta._usuarios) == 1
        assert len(sistema_com_usuario_e_conta._contas) == 1
        assert sistema_com_usuario_e_conta._conta_atual is not None

    def test_ambiente_teste_fixture(self, ambiente_teste: dict[str, str]) -> None:
        """Testa fixture de ambiente de teste."""
        assert ambiente_teste["ambiente"] == "teste"
        assert ambiente_teste["debug"] == "true"

    def test_configuracao_global_fixture(self, configuracao_global: dict[str, str]) -> None:
        """Testa fixture de configuração global."""
        assert configuracao_global["versao_sistema"] == "2.0.0"
        assert configuracao_global["banco_teste"] == "Banco PyTest"

    def test_dados_modulo_fixture(self, dados_modulo: dict[str, int]) -> None:
        """Testa fixture de dados do módulo."""
        assert dados_modulo["limite_saque"] == 50000
        assert dados_modulo["limite_saques_diarios"] == 3


# Testes parametrizados
class TestParametrizados:
    """Testes que usam fixtures parametrizadas."""

    def test_usuario_parametrizado(self, usuario_parametrizado: Usuario) -> None:
        """Testa fixture parametrizada de usuário."""
        assert len(usuario_parametrizado.nome) > 0
        assert len(usuario_parametrizado.cpf) == 11
        assert usuario_parametrizado.data_nascimento == "01/01/1990"

    def test_valores_deposito(self, valores_deposito: float, usuario_padrao: Usuario) -> None:
        """Testa fixture parametrizada de valores de depósito."""
        conta = ContaCorrente(usuario_padrao)
        resultado = conta.depositar(valores_deposito)

        assert resultado is True
        assert conta._saldo_centavos == int(valores_deposito * 100)

    def test_dados_conta(self, dados_conta: tuple[str, int]) -> None:
        """Testa fixture parametrizada de dados de conta."""
        agencia, numero = dados_conta
        assert agencia == "0001"
        assert numero in [1, 2, 3]
