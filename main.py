from datetime import datetime


class Usuario:
    """Classe que representa um usuário (cliente) do banco."""

    def __init__(self, nome: str, data_nascimento: str, cpf: str, endereco: str) -> None:
        self.nome: str = nome
        self.data_nascimento: str = data_nascimento
        self.cpf: str = self._formatar_cpf(cpf)
        self.endereco: str = endereco

    def _formatar_cpf(self, cpf: str) -> str:
        """Remove formatação do CPF e armazena apenas números."""
        return "".join(filter(str.isdigit, cpf))

    def get_cpf_formatado(self) -> str:
        """Retorna CPF formatado para exibição."""
        cpf = self.cpf
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

    def __str__(self) -> str:
        return f"{self.nome} - CPF: {self.get_cpf_formatado()}"


class ContaCorrente:
    """Classe que representa uma conta corrente."""

    _contador_contas: int = 1

    def __init__(self, usuario: Usuario, agencia: str = "0001") -> None:
        self.agencia: str = agencia
        self.numero_conta: int = ContaCorrente._contador_contas
        self.usuario: Usuario = usuario
        self._saldo_centavos: int = 0
        self._historico: list[dict[str, str]] = []
        self._limite_saque_diario_centavos: int = 50000  # R$ 500,00
        self._saques_realizados_hoje: int = 0
        self._limite_saques_diarios: int = 3
        self._data_ultimo_saque: str = ""

        ContaCorrente._contador_contas += 1

    def _real_para_centavos(self, valor: float) -> int:
        """Converte valor em reais para centavos."""
        return round(valor * 100)

    def _centavos_para_real(self, centavos: int) -> str:
        """Converte centavos para formato de reais."""
        reais = centavos // 100
        cents = centavos % 100
        return f"{reais}.{cents:02d}"

    def _formatar_moeda(self, centavos: int) -> str:
        """Formata centavos para exibição em moeda brasileira."""
        return f"R$ {self._centavos_para_real(centavos)}"

    def depositar(self, valor: float) -> bool:
        """
        Realiza depósito na conta.

        Args:
            valor: Valor a ser depositado em reais (deve ser positivo)

        Returns:
            bool: True se o depósito foi realizado com sucesso
        """
        if valor <= 0:
            print("❌ Erro: O valor do depósito deve ser positivo!")
            return False

        valor_centavos = self._real_para_centavos(valor)
        self._saldo_centavos += valor_centavos

        # Registra no histórico
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self._historico.append(
            {
                "tipo": "DEPÓSITO",
                "valor": self._formatar_moeda(valor_centavos),
                "data": timestamp,
                "saldo_pos": self._formatar_moeda(self._saldo_centavos),
            }
        )

        print("✅ Depósito realizado com sucesso!")
        print(f"💰 Valor depositado: {self._formatar_moeda(valor_centavos)}")
        print(f"💳 Saldo atual: {self._formatar_moeda(self._saldo_centavos)}")
        return True

    def sacar(self, valor: float) -> bool:
        """
        Realiza saque da conta com validações de limite e saldo.

        Args:
            valor: Valor a ser sacado em reais

        Returns:
            bool: True se o saque foi realizado com sucesso
        """
        if valor <= 0:
            print("❌ Erro: O valor do saque deve ser positivo!")
            return False

        valor_centavos = self._real_para_centavos(valor)
        data_hoje = datetime.now().strftime("%d/%m/%Y")

        # Reset contador se mudou o dia
        if self._data_ultimo_saque != data_hoje:
            self._saques_realizados_hoje = 0
            self._data_ultimo_saque = data_hoje

        # Validação de limite de saques diários
        if self._saques_realizados_hoje >= self._limite_saques_diarios:
            print(f"❌ Erro: Limite de {self._limite_saques_diarios} saques diários atingido!")
            return False

        # Validação de limite por saque
        if valor_centavos > self._limite_saque_diario_centavos:
            print(
                f"❌ Erro: Valor excede o limite máximo de {self._formatar_moeda(self._limite_saque_diario_centavos)}",
                " por saque!",
            )
            return False

        # Validação de saldo
        if valor_centavos > self._saldo_centavos:
            print("❌ Erro: Saldo insuficiente para realizar o saque!")
            print(f"💳 Saldo atual: {self._formatar_moeda(self._saldo_centavos)}")
            return False

        # Realiza o saque
        self._saldo_centavos -= valor_centavos
        self._saques_realizados_hoje += 1

        # Registra no histórico
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self._historico.append(
            {
                "tipo": "SAQUE",
                "valor": self._formatar_moeda(valor_centavos),
                "data": timestamp,
                "saldo_pos": self._formatar_moeda(self._saldo_centavos),
            }
        )

        print("✅ Saque realizado com sucesso!")
        print(f"💸 Valor sacado: {self._formatar_moeda(valor_centavos)}")
        print(f"💳 Saldo atual: {self._formatar_moeda(self._saldo_centavos)}")
        print(f"📊 Saques restantes hoje: {self._limite_saques_diarios - self._saques_realizados_hoje}")
        return True

    def visualizar_extrato(self) -> None:
        """Exibe o extrato completo da conta com todas as operações."""
        print("\n" + "=" * 70)
        print("📋 EXTRATO BANCÁRIO")
        print("=" * 70)
        print(f"👤 Titular: {self.usuario.nome}")
        print(f"📄 CPF: {self.usuario.get_cpf_formatado()}")
        print(f"🏦 Agência: {self.agencia}")
        print(f"🔢 Conta: {self.numero_conta}")
        print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("-" * 70)

        if not self._historico:
            print("📝 Nenhuma movimentação registrada.")
        else:
            print("📊 MOVIMENTAÇÕES:")
            print("-" * 70)
            for operacao in self._historico:
                tipo_icon = "📈" if operacao["tipo"] == "DEPÓSITO" else "📉"
                print(f"{tipo_icon} {operacao['tipo']}")
                print(f"   💰 Valor: {operacao['valor']}")
                print(f"   📅 Data: {operacao['data']}")
                print(f"   💳 Saldo: {operacao['saldo_pos']}")
                print("-" * 35)

        print(f"💰 SALDO ATUAL: {self._formatar_moeda(self._saldo_centavos)}")
        print("=" * 70)

    def get_saldo_formatado(self) -> str:
        """Retorna o saldo atual formatado."""
        return self._formatar_moeda(self._saldo_centavos)

    def get_info(self) -> dict[str, str]:
        """Retorna informações básicas da conta."""
        return {
            "titular": self.usuario.nome,
            "cpf": self.usuario.get_cpf_formatado(),
            "agencia": self.agencia,
            "conta": str(self.numero_conta),
            "saldo": self._formatar_moeda(self._saldo_centavos),
        }


class SistemaBancario:
    """Sistema bancário principal que gerencia usuários e contas."""

    def __init__(self) -> None:
        self._usuarios: list[Usuario] = []
        self._contas: list[ContaCorrente] = []
        self._conta_atual: ContaCorrente | None = None

    def criar_usuario(self, nome: str, data_nascimento: str, cpf: str, endereco: str) -> bool:
        """
        Cria um novo usuário.

        Args:
            nome: Nome completo do usuário
            data_nascimento: Data no formato DD/MM/AAAA
            cpf: CPF do usuário (apenas números)
            endereco: Endereço no formato: logradouro, nro - bairro - cidade/sigla estado

        Returns:
            bool: True se o usuário foi criado com sucesso
        """
        # Remove formatação do CPF para verificação
        cpf_numeros = "".join(filter(str.isdigit, cpf))

        # Verifica se CPF já existe
        if self._buscar_usuario_por_cpf(cpf_numeros):
            print(f"❌ Erro: Usuário com CPF {cpf} já existe!")
            return False

        usuario = Usuario(nome, data_nascimento, cpf_numeros, endereco)
        self._usuarios.append(usuario)
        print(f"✅ Usuário {nome} criado com sucesso!")
        return True

    def _buscar_usuario_por_cpf(self, cpf: str) -> Usuario | None:
        """Busca usuário pelo CPF."""
        cpf_numeros = "".join(filter(str.isdigit, cpf))
        for usuario in self._usuarios:
            if usuario.cpf == cpf_numeros:
                return usuario
        return None

    def criar_conta_corrente(self, cpf: str) -> bool:
        """
        Cria uma conta corrente vinculada a um usuário.

        Args:
            cpf: CPF do usuário para vincular a conta

        Returns:
            bool: True se a conta foi criada com sucesso
        """
        usuario = self._buscar_usuario_por_cpf(cpf)
        if not usuario:
            print(f"❌ Erro: Usuário com CPF {cpf} não encontrado!")
            return False

        conta = ContaCorrente(usuario)
        self._contas.append(conta)
        print(f"✅ Conta {conta.numero_conta} criada com sucesso para {usuario.nome}!")
        print(f"🏦 Agência: {conta.agencia} - Conta: {conta.numero_conta}")
        return True

    def selecionar_conta(self, agencia: str, numero_conta: int) -> bool:
        """
        Seleciona uma conta para operações.

        Args:
            agencia: Número da agência
            numero_conta: Número da conta

        Returns:
            bool: True se a conta foi selecionada com sucesso
        """
        for conta in self._contas:
            if conta.agencia == agencia and conta.numero_conta == numero_conta:
                self._conta_atual = conta
                info = conta.get_info()
                print(f"✅ Conta selecionada: {info['agencia']}-{info['conta']} - {info['titular']}")
                return True

        print(f"❌ Erro: Conta {agencia}-{numero_conta} não encontrada!")
        return False

    def get_conta_atual(self) -> ContaCorrente | None:
        """Retorna a conta atualmente selecionada."""
        return self._conta_atual

    def listar_usuarios(self) -> None:
        """Lista todos os usuários cadastrados."""
        if not self._usuarios:
            print("📝 Nenhum usuário cadastrado no sistema.")
            return

        print("\n👥 USUÁRIOS CADASTRADOS:")
        print("-" * 60)
        for usuario in self._usuarios:
            print(f"👤 {usuario}")

    def listar_contas(self) -> None:
        """Lista todas as contas do sistema."""
        if not self._contas:
            print("📝 Nenhuma conta cadastrada no sistema.")
            return

        print("\n🏦 CONTAS CADASTRADAS:")
        print("-" * 80)
        for conta in self._contas:
            info = conta.get_info()
            print(f"🏦 {info['agencia']}-{info['conta']} | {info['titular']} | {info['cpf']} | {info['saldo']}")


# Funções para operações bancárias (versão modularizada)
def depositar(conta: ContaCorrente, valor: float) -> bool:
    """Função para realizar depósito."""
    return conta.depositar(valor)


def sacar(conta: ContaCorrente, valor: float) -> bool:
    """Função para realizar saque."""
    return conta.sacar(valor)


def visualizar_historico(conta: ContaCorrente) -> None:
    """Função para visualizar o histórico/extrato."""
    conta.visualizar_extrato()


# Funções utilitárias
def exibir_menu() -> None:
    """Exibe o menu principal do sistema."""
    print("\n" + "=" * 60)
    print("🏦 SISTEMA BANCÁRIO - VERSÃO 2.0")
    print("=" * 60)
    print("1️⃣  Criar Usuário")
    print("2️⃣  Criar Conta Corrente")
    print("3️⃣  Selecionar Conta")
    print("4️⃣  Depositar")
    print("5️⃣  Sacar")
    print("6️⃣  Visualizar Extrato")
    print("7️⃣  Listar Usuários")
    print("8️⃣  Listar Contas")
    print("9️⃣  Sair")
    print("=" * 60)


def obter_valor_monetario(prompt: str) -> float | None:
    """Obtém um valor monetário válido do usuário."""
    try:
        valor_str = input(prompt).replace(",", ".")
        valor = float(valor_str)
        if valor <= 0:
            print("❌ Erro: O valor deve ser positivo!")
            return None
        return valor
    except ValueError:
        print("❌ Erro: Valor inválido! Digite um número válido.")
        return None


def validar_cpf(cpf: str) -> bool:
    """Valida formato básico do CPF."""
    cpf_numeros = "".join(filter(str.isdigit, cpf))
    return len(cpf_numeros) == 11


def main() -> None:  # noqa: C901
    """Função principal do sistema bancário."""
    sistema = SistemaBancario()

    print("🏦 Bem-vindo ao Sistema Bancário v2.0!")
    print("📝 Sistema modularizado com usuários e contas correntes")

    while True:
        exibir_menu()

        try:
            opcao = input("🔍 Escolha uma opção: ").strip()

            if opcao == "1":
                print("\n👤 CRIAR NOVO USUÁRIO")
                nome = input("📝 Nome completo: ").strip()
                data_nascimento = input("📅 Data de nascimento (DD/MM/AAAA): ").strip()
                cpf = input("📄 CPF (apenas números): ").strip()

                if not validar_cpf(cpf):
                    print("❌ Erro: CPF deve ter 11 dígitos!")
                    continue

                print("🏠 Endereço:")
                logradouro = input("   Logradouro: ").strip()
                numero = input("   Número: ").strip()
                bairro = input("   Bairro: ").strip()
                cidade = input("   Cidade: ").strip()
                estado = input("   Estado (sigla): ").strip()

                endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"

                if nome and data_nascimento and cpf:
                    sistema.criar_usuario(nome, data_nascimento, cpf, endereco)
                else:
                    print("❌ Erro: Todos os campos são obrigatórios!")

            elif opcao == "2":
                print("\n🏦 CRIAR CONTA CORRENTE")
                cpf = input("📄 CPF do usuário: ").strip()

                if not validar_cpf(cpf):
                    print("❌ Erro: CPF deve ter 11 dígitos!")
                    continue

                sistema.criar_conta_corrente(cpf)

            elif opcao == "3":
                print("\n🔍 SELECIONAR CONTA")
                sistema.listar_contas()
                agencia = input("🏦 Digite o número da agência: ").strip()
                try:
                    numero_conta = int(input("🔢 Digite o número da conta: ").strip())
                    sistema.selecionar_conta(agencia, numero_conta)
                except ValueError:
                    print("❌ Erro: Número da conta deve ser um número!")

            elif opcao == "4":
                conta_atual = sistema.get_conta_atual()
                if not conta_atual:
                    print("❌ Erro: Nenhuma conta selecionada! Selecione uma conta primeiro.")
                    continue

                print(f"\n💰 DEPÓSITO - Conta: {conta_atual.agencia}-{conta_atual.numero_conta}")
                valor = obter_valor_monetario("💵 Digite o valor para depósito (R$): ")
                if valor is not None:
                    depositar(conta_atual, valor)

            elif opcao == "5":
                conta_atual = sistema.get_conta_atual()
                if not conta_atual:
                    print("❌ Erro: Nenhuma conta selecionada! Selecione uma conta primeiro.")
                    continue

                print(f"\n💸 SAQUE - Conta: {conta_atual.agencia}-{conta_atual.numero_conta}")
                print(f"💳 Saldo atual: {conta_atual.get_saldo_formatado()}")
                valor = obter_valor_monetario("💵 Digite o valor para saque (R$): ")
                if valor is not None:
                    sacar(conta_atual, valor)

            elif opcao == "6":
                conta_atual = sistema.get_conta_atual()
                if not conta_atual:
                    print("❌ Erro: Nenhuma conta selecionada! Selecione uma conta primeiro.")
                    continue

                visualizar_historico(conta_atual)

            elif opcao == "7":
                sistema.listar_usuarios()

            elif opcao == "8":
                sistema.listar_contas()

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
