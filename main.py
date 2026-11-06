class Servico:
    """Registro de um serviço de documentação/cidadania."""

    def __init__(self, id_, titulo, categoria, descricao, requisitos,
                 local, prazo, custo):
        self.id = id_
        self.titulo = titulo
        self.categoria = categoria
        self.descricao = descricao
        self.requisitos = requisitos
        self.local = local
        self.prazo = prazo
        self.custo = custo

    def exibir(self):
        print(f"  ID:         {self.id}")
        print(f"  Título:     {self.titulo}")
        print(f"  Categoria:  {self.categoria}")
        print(f"  Descrição:  {self.descricao}")
        print(f"  Requisitos: {self.requisitos}")
        print(f"  Local:      {self.local}")
        print(f"  Prazo:      {self.prazo}")
        print(f"  Custo:      {self.custo}")


class No:
    def __init__(self, dado):
        self.dado = dado
        self.proximo = None


class ListaEncadeada:
    def __init__(self):
        self.cabeca = None
        self.cauda = None
        self.tamanho = 0

    def esta_vazia(self):
        return self.cabeca is None

    def inserir_fim(self, dado):
        novo = No(dado)
        if self.cabeca is None:
            self.cabeca = novo
            self.cauda = novo
        else:
            self.cauda.proximo = novo
            self.cauda = novo
        self.tamanho += 1

    def percorrer(self):
        atual = self.cabeca
        while atual is not None:
            yield atual.dado
            atual = atual.proximo

    def buscar_por_id(self, id_):
        atual = self.cabeca
        while atual is not None:
            if atual.dado.id == id_:
                return atual.dado
            atual = atual.proximo
        return None

    def pesquisar(self, campo, termo):
        termo = termo.lower()
        resultados = []
        atual = self.cabeca
        while atual is not None:
            valor = getattr(atual.dado, campo).lower()
            if termo in valor:
                resultados.append(atual.dado)
            atual = atual.proximo
        return resultados

    def remover(self, id_):
        anterior = None
        atual = self.cabeca
        while atual is not None:
            if atual.dado.id == id_:
                if anterior is None:          # remoção da cabeça
                    self.cabeca = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                if atual is self.cauda:       # remoção da cauda
                    self.cauda = anterior
                atual.proximo = None
                self.tamanho -= 1
                return True
            anterior = atual
            atual = atual.proximo
        return False

    def ordenar_por_id(self):
        self.cabeca = self._merge_sort(self.cabeca)
        atual = self.cabeca
        self.cauda = None
        while atual is not None:
            self.cauda = atual
            atual = atual.proximo

    def _merge_sort(self, cabeca):
        if cabeca is None or cabeca.proximo is None:
            return cabeca
        meio = self._dividir(cabeca)
        direita = meio.proximo
        meio.proximo = None
        esquerda = self._merge_sort(cabeca)
        direita = self._merge_sort(direita)
        return self._mesclar(esquerda, direita)

    @staticmethod
    def _dividir(cabeca):
        lento = cabeca
        rapido = cabeca.proximo
        while rapido is not None and rapido.proximo is not None:
            lento = lento.proximo
            rapido = rapido.proximo.proximo
        return lento

    @staticmethod
    def _mesclar(a, b):
        sentinela = No(None)
        ponta = sentinela
        while a is not None and b is not None:
            if a.dado.id <= b.dado.id:
                ponta.proximo = a
                a = a.proximo
            else:
                ponta.proximo = b
                b = b.proximo
            ponta = ponta.proximo
        ponta.proximo = a if a is not None else b
        return sentinela.proximo

    def contar_por_categoria(self):
        contagem = {}
        for s in self.percorrer():
            chave = s.categoria.strip().title()
            contagem[chave] = contagem.get(chave, 0) + 1
        return contagem

def ler_inteiro_positivo(mensagem):
    texto = input(mensagem).strip()
    if not texto.isdigit() or int(texto) <= 0:
        print("  [!] Entrada inválida: informe um número inteiro positivo.")
        return None
    return int(texto)

def ler_texto(mensagem, atual=None):
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        if atual is not None:
            return atual
        print("  [!] Este campo não pode ficar vazio.")

def cadastrar(lista):
    print("\n--- CADASTRAR SERVIÇO ---")
    id_ = ler_inteiro_positivo("ID (inteiro positivo): ")
    if id_ is None:
        return
    if lista.buscar_por_id(id_) is not None:
        print(f"  [!] Já existe um serviço com ID {id_}. Cadastro cancelado.")
        return
    servico = Servico(
        id_,
        ler_texto("Título: "),
        ler_texto("Categoria (ex.: Identidade, Trabalho, Previdência): "),
        ler_texto("Descrição: "),
        ler_texto("Requisitos: "),
        ler_texto("Local de atendimento: "),
        ler_texto("Prazo (ex.: 10 dias úteis): "),
        ler_texto("Custo (ex.: Gratuito, R$ 80,00): "),
    )
    lista.inserir_fim(servico)
    print("  Serviço cadastrado com sucesso!")


def consultar_por_id(lista):
    print("\n--- CONSULTAR POR ID ---")
    if lista.esta_vazia():
        print("  A lista está vazia. Cadastre um serviço primeiro.")
        return
    id_ = ler_inteiro_positivo("ID: ")
    if id_ is None:
        return
    servico = lista.buscar_por_id(id_)
    if servico is None:
        print(f"  Nenhum serviço encontrado com ID {id_}.")
    else:
        servico.exibir()


def pesquisar(lista):
    print("\n--- PESQUISAR ---")
    if lista.esta_vazia():
        print("  A lista está vazia. Cadastre um serviço primeiro.")
        return
    print("  1 - Por título")
    print("  2 - Por categoria")
    escolha = input("  Pesquisar por: ").strip()
    if escolha == "1":
        campo = "titulo"
    elif escolha == "2":
        campo = "categoria"
    else:
        print("  [!] Opção inválida.")
        return
    termo = ler_texto("  Termo de busca: ")
    resultados = lista.pesquisar(campo, termo)
    if not resultados:
        print(f"  Nenhum resultado para '{termo}'.")
        return
    print(f"  {len(resultados)} resultado(s) encontrado(s):\n")
    for s in resultados:
        s.exibir()
        print("  " + "-" * 40)


def atualizar(lista):
    print("\n--- ATUALIZAR SERVIÇO ---")
    if lista.esta_vazia():
        print("  A lista está vazia. Cadastre um serviço primeiro.")
        return
    id_ = ler_inteiro_positivo("ID do serviço a atualizar: ")
    if id_ is None:
        return
    s = lista.buscar_por_id(id_)
    if s is None:
        print(f"  Nenhum serviço encontrado com ID {id_}.")
        return
    print("  Dados atuais:")
    s.exibir()
    print("\n  (Pressione ENTER para manter o valor atual. O ID não pode ser alterado.)")
    s.titulo = ler_texto("Novo título: ", s.titulo)
    s.categoria = ler_texto("Nova categoria: ", s.categoria)
    s.descricao = ler_texto("Nova descrição: ", s.descricao)
    s.requisitos = ler_texto("Novos requisitos: ", s.requisitos)
    s.local = ler_texto("Novo local: ", s.local)
    s.prazo = ler_texto("Novo prazo: ", s.prazo)
    s.custo = ler_texto("Novo custo: ", s.custo)
    print("  Serviço atualizado com sucesso!")


def excluir(lista):
    print("\n--- EXCLUIR SERVIÇO ---")
    if lista.esta_vazia():
        print("  A lista está vazia. Nada para excluir.")
        return
    id_ = ler_inteiro_positivo("ID do serviço a excluir: ")
    if id_ is None:
        return
    if lista.remover(id_):
        print("  Serviço excluído com sucesso!")
    else:
        print(f"  Nenhum serviço encontrado com ID {id_}.")


def listar(lista):
    print("\n--- LISTA DE SERVIÇOS ---")
    if lista.esta_vazia():
        print("  A lista está vazia.")
        return
    for s in lista.percorrer():
        s.exibir()
        print("  " + "-" * 40)


def ordenar(lista):
    print("\n--- ORDENAR POR ID (Merge Sort) ---")
    if lista.esta_vazia():
        print("  A lista está vazia. Nada para ordenar.")
        return
    lista.ordenar_por_id()
    print("  Lista ordenada por ID (crescente):\n")
    for s in lista.percorrer():
        print(f"  [{s.id}] {s.titulo} ({s.categoria})")


def analisar(lista):
    print("\n--- ANÁLISE ---")
    if lista.esta_vazia():
        print("  A lista está vazia. Sem dados para analisar.")
        return
    print(f"  Total de serviços cadastrados: {lista.tamanho}")
    print("  Quantidade por categoria:")
    for categoria, qtd in sorted(lista.contar_por_categoria().items()):
        print(f"    - {categoria}: {qtd}")


def carregar_exemplos(lista):
    exemplos = [
        (32, "Emissão de CPF", "Identidade", "Cadastro de Pessoa Física.",
         "Documento com foto e título de eleitor", "Agências dos Correios / Receita Federal",
         "No mesmo dia", "R$ 7,00"),
        (59, "Segunda via de RG", "Identidade", "Emissão de nova identidade.",
         "Certidão de nascimento ou casamento e comprovante de residência",
         "Poupatempo", "10 dias úteis", "Gratuito"),
        (30, "Carteira de Trabalho Digital", "Trabalho", "Acesso pelo aplicativo gov.br.",
         "CPF e conta gov.br", "Online ", "No mesmo dia", "gratuito"),
        (4, "Aposentadoria por idade", "Previdência", "Pedido de benefício no INSS.",
         "Idade mínima e tempo de contribuição", "Aplicativo Meu INSS ou agência",
         "Até 45 dias", "Gratuito"),
    ]
    adicionados = 0
    for e in exemplos:
        if lista.buscar_por_id(e[0]) is None:
            lista.inserir_fim(Servico(*e))
            adicionados += 1
    print(f"  {adicionados} serviço(s) de exemplo carregado(s).")

def exibir_menu():
    print("\n" + "=" * 44)
    print("   CITIZEN ASSIST AI - Documentação e Cidadania")
    print("=" * 44)
    print("  1 - Cadastrar serviço")
    print("  2 - Consultar por ID")
    print("  3 - Pesquisar (título ou categoria)")
    print("  4 - Atualizar serviço")
    print("  5 - Excluir serviço")
    print("  6 - Listar todos")
    print("  7 - Ordenar por ID (Merge Sort)")
    print("  8 - Análise (indicadores)")
    print("  9 - Carregar dados de exemplo")
    print("  0 - Sair")

def main():
    lista = ListaEncadeada()
    acoes = {
        "1": cadastrar,
        "2": consultar_por_id,
        "3": pesquisar,
        "4": atualizar,
        "5": excluir,
        "6": listar,
        "7": ordenar,
        "8": analisar,
        "9": carregar_exemplos,
    }
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("\nEncerrando o Citizen Assist AI. Até logo!")
            break
        acao = acoes.get(opcao)
        if acao is None:
            print("  [!] Opção inválida. Escolha um número de 0 a 9.")
        else:
            acao(lista)
            
if __name__ == "__main__":
    main()