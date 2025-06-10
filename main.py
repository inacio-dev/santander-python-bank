from datetime import datetime


class ContaBancaria:
    """Classe que representa uma conta bancária com operações básicas."""

    def __init__(self, numero_conta: str, titular: str) -> None:
        self._numero_conta: str = numero_conta
        self._titular: str = titular
        self._saldo_centavos: int = 0  # Saldo em centavos
        self._historico: list[dict[str, str]] = []
        self._limite_saque_diario_centavos: int = 50000  # R$ 500,00 em centavos
        self._saques_realizados_hoje: int = 0
        self._limite_saques_diarios: int = 3
        self._data_ultimo_saque: str = ""

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
            print(
                f"❌ Erro: Limite de {self._limite_saques_diarios} saques diários atingido!"
            )
            return False

        # Validação de limite por saque
        if valor_centavos > self._limite_saque_diario_centavos:
            print(
                f"❌ Erro: Valor excede o limite máximo de {self._formatar_moeda(self._limite_saque_diario_centavos)} ",
                "por saque!",
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
        print(
            f"📊 Saques restantes hoje: {self._limite_saques_diarios - self._saques_realizados_hoje}"
        )
        return True

    def visualizar_extrato(self) -> None:
        """Exibe o extrato completo da conta com todas as operações."""
        print("\n" + "=" * 60)
        print("📋 EXTRATO BANCÁRIO")
        print("=" * 60)
        print(f"👤 Titular: {self._titular}")
        print(f"🏦 Conta: {self._numero_conta}")
        print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("-" * 60)

        if not self._historico:
            print("📝 Nenhuma movimentação registrada.")
        else:
            print("📊 MOVIMENTAÇÕES:")
            print("-" * 60)
            for operacao in self._historico:
                tipo_icon = "📈" if operacao["tipo"] == "DEPÓSITO" else "📉"
                print(f"{tipo_icon} {operacao['tipo']}")
                print(f"   💰 Valor: {operacao['valor']}")
                print(f"   📅 Data: {operacao['data']}")
                print(f"   💳 Saldo: {operacao['saldo_pos']}")
                print("-" * 30)

        print(f"💰 SALDO ATUAL: {self._formatar_moeda(self._saldo_centavos)}")
        print("=" * 60)

    def get_saldo_centavos(self) -> int:
        """Retorna o saldo atual da conta em centavos."""
        return self._saldo_centavos

    def get_saldo_formatado(self) -> str:
        """Retorna o saldo atual formatado em reais."""
        return self._formatar_moeda(self._saldo_centavos)

    def get_info(self) -> dict[str, str]:
        """Retorna informações básicas da conta."""
        return {
            "titular": self._titular,
            "conta": self._numero_conta,
            "saldo": self._formatar_moeda(self._saldo_centavos),
        }


class SistemaBancario:
    """Sistema bancário principal que gerencia as contas."""

    def __init__(self) -> None:
        self._contas: dict[str, ContaBancaria] = {}
        self._conta_atual: ContaBancaria | None = None

    def criar_conta(self, numero_conta: str, titular: str) -> bool:
        """Cria uma nova conta bancária."""
        if numero_conta in self._contas:
            print(f"❌ Erro: Conta {numero_conta} já existe!")
            return False

        self._contas[numero_conta] = ContaBancaria(numero_conta, titular)
        print(f"✅ Conta {numero_conta} criada com sucesso para {titular}!")
        return True

    def selecionar_conta(self, numero_conta: str) -> bool:
        """Seleciona uma conta para operações."""
        if numero_conta not in self._contas:
            print(f"❌ Erro: Conta {numero_conta} não encontrada!")
            return False

        self._conta_atual = self._contas[numero_conta]
        info = self._conta_atual.get_info()
        print(f"✅ Conta selecionada: {info['conta']} - {info['titular']}")
        return True

    def get_conta_atual(self) -> ContaBancaria | None:
        """Retorna a conta atualmente selecionada."""
        return self._conta_atual

    def listar_contas(self) -> None:
        """Lista todas as contas do sistema."""
        if not self._contas:
            print("📝 Nenhuma conta cadastrada no sistema.")
            return

        print("\n📋 CONTAS CADASTRADAS:")
        print("-" * 40)
        for conta in self._contas.values():
            info = conta.get_info()
            print(f"🏦 {info['conta']} - {info['titular']} - {info['saldo']}")


def exibir_menu() -> None:
    """Exibe o menu principal do sistema."""
    print("\n" + "=" * 50)
    print("🏦 SISTEMA BANCÁRIO")
    print("=" * 50)
    print("1️⃣  Criar Conta")
    print("2️⃣  Selecionar Conta")
    print("3️⃣  Depositar")
    print("4️⃣  Sacar")
    print("5️⃣  Visualizar Extrato")
    print("6️⃣  Listar Contas")
    print("7️⃣  Sair")
    print("=" * 50)


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


def main() -> None:  # noqa: C901
    """Função principal do sistema bancário."""
    sistema = SistemaBancario()

    # Criar uma conta padrão para demonstração
    sistema.criar_conta("12345-6", "Usuário Demonstração")

    print("🏦 Bem-vindo ao Sistema Bancário!")
    print("📝 Conta demonstrativa criada: 12345-6")

    while True:
        exibir_menu()

        try:
            opcao = input("🔍 Escolha uma opção: ").strip()

            if opcao == "1":
                print("\n📝 CRIAR NOVA CONTA")
                numero_conta = input("🏦 Digite o número da conta: ").strip()
                titular = input("👤 Digite o nome do titular: ").strip()

                if numero_conta and titular:
                    sistema.criar_conta(numero_conta, titular)
                else:
                    print(
                        "❌ Erro: Número da conta e nome do titular são obrigatórios!"
                    )

            elif opcao == "2":
                print("\n🔍 SELECIONAR CONTA")
                sistema.listar_contas()
                numero_conta = input("🏦 Digite o número da conta: ").strip()
                sistema.selecionar_conta(numero_conta)

            elif opcao == "3":
                conta_atual = sistema.get_conta_atual()
                if not conta_atual:
                    print(
                        "❌ Erro: Nenhuma conta selecionada! Selecione uma conta primeiro."
                    )
                    continue

                print(f"\n💰 DEPÓSITO - Conta: {conta_atual.get_info()['conta']}")
                valor = obter_valor_monetario("💵 Digite o valor para depósito (R$): ")
                if valor is not None:
                    conta_atual.depositar(valor)

            elif opcao == "4":
                conta_atual = sistema.get_conta_atual()
                if not conta_atual:
                    print(
                        "❌ Erro: Nenhuma conta selecionada! Selecione uma conta primeiro."
                    )
                    continue

                print(f"\n💸 SAQUE - Conta: {conta_atual.get_info()['conta']}")
                print(f"💳 Saldo atual: {conta_atual.get_saldo_formatado()}")
                valor = obter_valor_monetario("💵 Digite o valor para saque (R$): ")
                if valor is not None:
                    conta_atual.sacar(valor)

            elif opcao == "5":
                conta_atual = sistema.get_conta_atual()
                if not conta_atual:
                    print(
                        "❌ Erro: Nenhuma conta selecionada! Selecione uma conta primeiro."
                    )
                    continue

                conta_atual.visualizar_extrato()

            elif opcao == "6":
                sistema.listar_contas()

            elif opcao == "7":
                print("👋 Obrigado por usar o Sistema Bancário!")
                break

            else:
                print("❌ Opção inválida! Digite um número de 1 a 7.")

        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")


if __name__ == "__main__":
    main()
