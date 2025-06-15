from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    """Classe que representa um cliente do banco."""

    def __init__(self, endereco: str) -> None:
        self.endereco: str = endereco
        self.contas: list[Conta] = []

    def realizar_transacao(self, conta: "Conta", transacao: "Transacao") -> None:
        """Realiza uma transação em uma conta específica."""
        if len(conta.historico.transacoes) >= 10:
            print("❌ Erro: Limite de 10 transações por dia atingido!")
            return

        transacao.registrar(conta)

    def adicionar_conta(self, conta: "Conta") -> None:
        """Adiciona uma conta à lista de contas do cliente."""
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """Classe que representa uma pessoa física como cliente do banco."""

    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str) -> None:
        super().__init__(endereco)
        self.nome: str = nome
        self.data_nascimento: str = data_nascimento
        self.cpf: str = self._formatar_cpf(cpf)

    def _formatar_cpf(self, cpf: str) -> str:
        """Remove formatação do CPF e armazena apenas números."""
        return "".join(filter(str.isdigit, cpf))

    def get_cpf_formatado(self) -> str:
        """Retorna CPF formatado para exibição."""
        cpf = self.cpf
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    def __str__(self) -> str:
        return f"{self.nome} - CPF: {self.get_cpf_formatado()}"


class Conta:
    """Classe base que representa uma conta bancária."""

    _contador_contas: int = 1

    def __init__(self, cliente: Cliente, numero: int | None = None) -> None:
        self._saldo_centavos: int = 0
        self._numero: int = numero if numero else Conta._contador_contas
        self._agencia: str = "0001"
        self._cliente: Cliente = cliente
        self._historico: Historico = Historico()

        if numero is None:
            Conta._contador_contas += 1

    @classmethod
    def nova_conta(cls, cliente: Cliente, numero: int) -> "Conta":
        """Método de classe para criar uma nova conta."""
        return cls(cliente, numero)

    @property
    def saldo(self) -> float:
        """Retorna o saldo em reais."""
        return self._saldo_centavos / 100

    @property
    def numero(self) -> int:
        """Retorna o número da conta."""
        return self._numero

    @property
    def agencia(self) -> str:
        """Retorna a agência."""
        return self._agencia

    @property
    def cliente(self) -> Cliente:
        """Retorna o cliente."""
        return self._cliente

    @property
    def historico(self) -> "Historico":
        """Retorna o histórico."""
        return self._historico

    def sacar(self, valor: float) -> bool:
        """Realiza saque da conta."""
        if valor <= 0:
            print("❌ Erro: O valor do saque deve ser positivo!")
            return False

        valor_centavos = int(valor * 100)

        if valor_centavos > self._saldo_centavos:
            print("❌ Erro: Saldo insuficiente para realizar o saque!")
            print(f"💳 Saldo atual: {self._formatar_moeda(self._saldo_centavos)}")
            return False

        self._saldo_centavos -= valor_centavos
        print("✅ Saque realizado com sucesso!")
        print(f"💸 Valor sacado: {self._formatar_moeda(valor_centavos)}")
        print(f"💳 Saldo atual: {self._formatar_moeda(self._saldo_centavos)}")
        return True

    def depositar(self, valor: float) -> bool:
        """Realiza depósito na conta."""
        if valor <= 0:
            print("❌ Erro: O valor do depósito deve ser positivo!")
            return False

        valor_centavos = int(valor * 100)
        self._saldo_centavos += valor_centavos

        print("✅ Depósito realizado com sucesso!")
        print(f"💰 Valor depositado: {self._formatar_moeda(valor_centavos)}")
        print(f"💳 Saldo atual: {self._formatar_moeda(self._saldo_centavos)}")
        return True

    def _formatar_moeda(self, centavos: int) -> str:
        """Formata centavos para exibição em moeda brasileira."""
        reais = centavos // 100
        cents = centavos % 100
        return f"R$ {reais}.{cents:02d}"

    def get_saldo_formatado(self) -> str:
        """Retorna o saldo atual formatado."""
        return self._formatar_moeda(self._saldo_centavos)


class ContaCorrente(Conta):
    """Classe que representa uma conta corrente com limites específicos."""

    def __init__(
        self, cliente: Cliente, numero: int | None = None, limite: float = 500.0, limite_saques: int = 3
    ) -> None:
        super().__init__(cliente, numero)
        self._limite_centavos: int = int(limite * 100)
        self._limite_saques: int = limite_saques
        self._saques_realizados_hoje: int = 0
        self._data_ultimo_saque: str = ""

    def sacar(self, valor: float) -> bool:
        """Realiza saque com validações específicas da conta corrente."""
        if valor <= 0:
            print("❌ Erro: O valor do saque deve ser positivo!")
            return False

        valor_centavos = int(valor * 100)
        data_hoje = datetime.now().strftime("%d/%m/%Y")

        # Reset contador se mudou o dia
        if self._data_ultimo_saque != data_hoje:
            self._saques_realizados_hoje = 0
            self._data_ultimo_saque = data_hoje

        # Validação de limite de saques diários
        if self._saques_realizados_hoje >= self._limite_saques:
            print(f"❌ Erro: Limite de {self._limite_saques} saques diários atingido!")
            return False

        # Validação de limite por saque
        if valor_centavos > self._limite_centavos:
            print(f"❌ Erro: Valor excede o limite máximo de {self._formatar_moeda(self._limite_centavos)} por saque!")
            return False

        # Validação de saldo
        if valor_centavos > self._saldo_centavos:
            print("❌ Erro: Saldo insuficiente para realizar o saque!")
            print(f"💳 Saldo atual: {self._formatar_moeda(self._saldo_centavos)}")
            return False

        # Realiza o saque
        self._saldo_centavos -= valor_centavos
        self._saques_realizados_hoje += 1

        print("✅ Saque realizado com sucesso!")
        print(f"💸 Valor sacado: {self._formatar_moeda(valor_centavos)}")
        print(f"💳 Saldo atual: {self._formatar_moeda(self._saldo_centavos)}")
        print(f"📊 Saques restantes hoje: {self._limite_saques - self._saques_realizados_hoje}")
        return True

    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome if isinstance(self.cliente, PessoaFisica) else 'Cliente'}
        """


class Historico:
    """Classe que representa o histórico de transações de uma conta."""

    def __init__(self) -> None:
        self._transacoes: list[Transacao] = []

    @property
    def transacoes(self) -> list["Transacao"]:
        """Retorna a lista de transações."""
        return self._transacoes

    def adicionar_transacao(self, transacao: "Transacao") -> None:
        """Adiciona uma transação ao histórico."""
        self._transacoes.append(transacao)

    def gerar_relatorio(self, tipo_transacao: str | None = None) -> str:
        """Gera relatório das transações."""
        if not self._transacoes:
            return "📝 Nenhuma movimentação registrada."

        relatorio = []
        for transacao in self._transacoes:
            if tipo_transacao is None or transacao.__class__.__name__.lower() == tipo_transacao.lower():
                relatorio.append(
                    f"{transacao.data_hora.strftime('%d/%m/%Y %H:%M:%S')} - "
                    f"{transacao.__class__.__name__}: R$ {transacao.valor:.2f}"
                )

        return "\n".join(relatorio) if relatorio else f"📝 Nenhuma transação do tipo '{tipo_transacao}' encontrada."

    def transacoes_do_dia(self) -> list["Transacao"]:
        """Retorna transações do dia atual."""
        hoje = datetime.now().date()
        return [t for t in self._transacoes if t.data_hora.date() == hoje]


class Transacao(ABC):
    """Classe abstrata base para transações."""

    def __init__(self, valor: float) -> None:
        self._valor: float = valor
        self.data_hora: datetime = datetime.now()

    @property
    def valor(self) -> float:
        """Valor da transação."""
        return self._valor

    @abstractmethod
    def registrar(self, conta: Conta) -> None:
        """Registra a transação na conta."""
        pass


class Saque(Transacao):
    """Classe que representa uma transação de saque."""

    def __init__(self, valor: float) -> None:
        super().__init__(valor)

    def registrar(self, conta: Conta) -> None:
        """Registra o saque na conta."""
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """Classe que representa uma transação de depósito."""

    def __init__(self, valor: float) -> None:
        super().__init__(valor)

    def registrar(self, conta: Conta) -> None:
        """Registra o depósito na conta."""
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)


def exibir_menu() -> None:
    """Exibe o menu principal do sistema."""
    print("\n" + "=" * 60)
    print("🏦 SISTEMA BANCÁRIO - VERSÃO 3.0 (CLASSES)")
    print("=" * 60)
    print("1️⃣  Criar Usuário")
    print("2️⃣  Criar Conta Corrente")
    print("3️⃣  Depositar")
    print("4️⃣  Sacar")
    print("5️⃣  Visualizar Extrato")
    print("6️⃣  Listar Usuários")
    print("7️⃣  Listar Contas")
    print("8️⃣  Relatório de Transações")
    print("9️⃣  Sair")
    print("=" * 60)


def filtrar_cliente(cpf: str, clientes: list[PessoaFisica]) -> PessoaFisica | None:
    """Filtra cliente por CPF."""
    cpf_numeros = "".join(filter(str.isdigit, cpf))
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf_numeros]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente: Cliente) -> Conta | None:
    """Recupera conta do cliente."""
    if not cliente.contas:
        print("\n❌ Cliente não possui conta!")
        return None

    if len(cliente.contas) == 1:
        return cliente.contas[0]

    # Se cliente tem múltiplas contas, listar para escolha
    print("\n🏦 Contas disponíveis:")
    for i, conta in enumerate(cliente.contas, 1):
        print(f"{i}. Conta {conta.numero} - Saldo: {conta.get_saldo_formatado()}")

    try:
        escolha = int(input("Escolha o número da conta: ")) - 1
        if 0 <= escolha < len(cliente.contas):
            return cliente.contas[escolha]
        else:
            print("❌ Opção inválida!")
            return None
    except ValueError:
        print("❌ Digite um número válido!")
        return None


def processar_deposito(clientes: list[PessoaFisica]) -> None:
    """Função para realizar depósito."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    try:
        valor = float(input("Informe o valor do depósito: "))
    except ValueError:
        print("❌ Valor inválido!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)


def processar_saque(clientes: list[PessoaFisica]) -> None:
    """Função para realizar saque."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("❌ Valor inválido!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes: list[PessoaFisica]) -> None:
    """Função para exibir extrato."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n" + "=" * 100)
    print("EXTRATO".center(100))
    print("=" * 100)

    transacoes = conta.historico.gerar_relatorio()
    print(transacoes)

    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("=" * 100)


def processar_criacao_usuario(clientes: list[PessoaFisica]) -> None:
    """Processa criação de novo usuário."""
    print("\n👤 CRIAR NOVO USUÁRIO")
    nome = input("📝 Nome completo: ").strip()
    data_nascimento = input("📅 Data de nascimento (DD/MM/AAAA): ").strip()
    cpf = input("📄 CPF (apenas números): ").strip()

    if not validar_cpf(cpf):
        print("❌ Erro: CPF deve ter 11 dígitos!")
        return

    cliente_existente = filtrar_cliente(cpf, clientes)
    if cliente_existente:
        print("❌ Erro: Já existe cliente com esse CPF!")
        return

    print("🏠 Endereço:")
    logradouro = input("   Logradouro: ").strip()
    numero = input("   Número: ").strip()
    bairro = input("   Bairro: ").strip()
    cidade = input("   Cidade: ").strip()
    estado = input("   Estado (sigla): ").strip()

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"

    if nome and data_nascimento and cpf:
        cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
        clientes.append(cliente)
        print(f"✅ Usuário {nome} criado com sucesso!")
    else:
        print("❌ Erro: Todos os campos são obrigatórios!")


def processar_criacao_conta(clientes: list[PessoaFisica], contas: list[Conta]) -> None:
    """Processa criação de conta corrente."""
    print("\n🏦 CRIAR CONTA CORRENTE")
    cpf = input("📄 CPF do usuário: ").strip()

    if not validar_cpf(cpf):
        print("❌ Erro: CPF deve ter 11 dígitos!")
        return

    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("❌ Erro: Cliente não encontrado!")
        return

    numero_conta = len(contas) + 1
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)

    print(f"✅ Conta {conta.numero} criada com sucesso para {cliente.nome}!")
    print(f"🏦 Agência: {conta.agencia} - Conta: {conta.numero}")


def listar_contas(contas: list[Conta]) -> None:
    """Função para listar todas as contas."""
    if not contas:
        print("\n📝 Nenhuma conta cadastrada.")
        return

    print("\n🏦 CONTAS CADASTRADAS:")
    print("-" * 100)
    for conta in contas:
        linha = f"Agência: {conta.agencia} | Conta: {conta.numero} | "
        if isinstance(conta.cliente, PessoaFisica):
            linha += f"Titular: {conta.cliente.nome} | Saldo: {conta.get_saldo_formatado()}"
        print(linha)


def validar_cpf(cpf: str) -> bool:
    """Valida formato básico do CPF."""
    cpf_numeros = "".join(filter(str.isdigit, cpf))
    return len(cpf_numeros) == 11


def listar_usuarios(clientes: list[PessoaFisica]) -> None:
    """Lista todos os usuários cadastrados."""
    if not clientes:
        print("📝 Nenhum usuário cadastrado no sistema.")
        return

    print("\n👥 USUÁRIOS CADASTRADOS:")
    print("-" * 60)
    for cliente in clientes:
        print(f"👤 {cliente}")


def gerar_relatorio_transacoes(clientes: list[PessoaFisica]) -> None:
    """Gera relatório detalhado de transações por tipo."""
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n❌ Cliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n📊 RELATÓRIO DE TRANSAÇÕES")
    print("=" * 50)

    tipo = input("Tipo de transação (deposito/saque/todas): ").lower()

    if tipo in ["deposito", "saque"]:
        relatorio = conta.historico.gerar_relatorio(tipo)
    else:
        relatorio = conta.historico.gerar_relatorio()

    print(relatorio)

    # Mostra transações do dia
    transacoes_hoje = conta.historico.transacoes_do_dia()
    print(f"\n📅 Transações hoje: {len(transacoes_hoje)}")
    print(f"💰 Saldo atual: {conta.get_saldo_formatado()}")


def main() -> None:
    """Função principal do sistema bancário."""
    clientes: list[PessoaFisica] = []
    contas: list[Conta] = []

    print("🏦 Bem-vindo ao Sistema Bancário v3.0!")
    print("📝 Sistema orientado a objetos com herança e polimorfismo")

    while True:
        exibir_menu()

        try:
            opcao = input("🔍 Escolha uma opção: ").strip()

            if opcao == "1":
                processar_criacao_usuario(clientes)

            elif opcao == "2":
                processar_criacao_conta(clientes, contas)

            elif opcao == "3":
                print("\n💰 REALIZAR DEPÓSITO")
                processar_deposito(clientes)

            elif opcao == "4":
                print("\n💸 REALIZAR SAQUE")
                processar_saque(clientes)

            elif opcao == "5":
                print("\n📋 VISUALIZAR EXTRATO")
                exibir_extrato(clientes)

            elif opcao == "6":
                listar_usuarios(clientes)

            elif opcao == "7":
                listar_contas(contas)

            elif opcao == "8":
                print("\n📊 RELATÓRIO DE TRANSAÇÕES")
                gerar_relatorio_transacoes(clientes)

            elif opcao == "9":
                print("👋 Obrigado por usar o Sistema Bancário!")
                break

            else:
                print("❌ Opção inválida! Digite um número de 1 a 9.")

        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")


if __name__ == "__main__":
    main()
