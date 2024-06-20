import pandas as pd
import os

def inicializar():
    arquivos = {
        'usuarios.xlsx': ['Nome', 'Email'],
        'usuarios_backup.xlsx': ['Nome', 'Email'],
        'produtos.xlsx': ['Nome', 'Preço'],
        'produtos_backup.xlsx': ['Nome', 'Preço'],
        'pedidos.xlsx': ['Cliente', 'Produto', 'Quantidade'],
        'estoque.xlsx': ['Produto', 'Quantidade']
    }

    for arquivo, colunas in arquivos.items():
        if not os.path.exists(arquivo):
            df = pd.DataFrame(columns=colunas)
            df.to_excel(arquivo, index=False)
            print(f'{arquivo} criado com sucesso!')
        else:
            print(f'{arquivo} já existe.')

def salvar_dados(df, nome_arquivo):
    df.to_excel(nome_arquivo, index=False)

def carregar_dados(nome_arquivo, nome_arquivo_bkp=None):
    if os.path.exists(nome_arquivo):
        return pd.read_excel(nome_arquivo)
    elif nome_arquivo_bkp and os.path.exists(nome_arquivo_bkp):
        print(f"Carregando dados do backup: {nome_arquivo_bkp}")
        return pd.read_excel(nome_arquivo_bkp)
    else:
        return pd.DataFrame()
    
def sincronizar_dados(df_bkp, nome_arquivo_principal):
    if os.path.exists(nome_arquivo_principal):
        df_principal = pd.read_excel(nome_arquivo_principal)
        df_sincronizado = pd.concat([df_principal, df_bkp]).drop_duplicates().reset_index(drop=True)
        salvar_dados(df_sincronizado, nome_arquivo_principal)
        print(f"Dados sincronizados com sucesso para {nome_arquivo_principal}!")
    else:
        print(f"O arquivo principal {nome_arquivo_principal} ainda não está disponível.")
    
def menu():
    while True:
        print("\nMenu Principal")
        print("(1) Usuário")
        print("(2) Produtos")
        print("(3) Pedidos")
        print("(4) Estoque")
        print("(0) Encerrar")
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            menu_usuario()
        elif escolha == '2':
            menu_produtos()
        elif escolha == '3':
            menu_pedidos()
        elif escolha == '4':
            menu_estoque()
        elif escolha == '0':
            break
        else:
            print("Opção inválida!")

def menu_usuario():
    df_usuarios,origem_usuarios  = carregar_dados('usuarios.xlsx', 'usuarios_backup.xlsx')
    while True:
        print("\nMenu Usuário")
        print("(1) Adicionar Usuário")
        print("(2) Atualizar Usuário")
        print("(3) Listar Usuários")
        print("(0) Voltar ao Menu Principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome: ")
            email = input("Email: ")
            novo_usuario = pd.DataFrame([{'Nome': nome, 'Email': email}])
            df_usuarios = pd.concat([df_usuarios, novo_usuario], ignore_index=True)
            salvar_dados(df_usuarios, 'usuarios.xlsx')
            if origem_usuarios == 'usuarios_backup.xlsx':
                sincronizar_dados(df_usuarios, 'usuarios.xlsx')
            salvar_dados(df_usuarios, 'usuarios_backup.xlsx')
            print("Usuário adicionado com sucesso!")
        elif escolha == '2':
            email = input("Email do usuário a ser atualizado: ")
            usuario = df_usuarios[df_usuarios['Email'] == email]
            if not usuario.empty:
                nome = input("Novo Nome: ")
                df_usuarios.loc[df_usuarios['Email'] == email, 'Nome'] = nome
                salvar_dados(df_usuarios, 'usuarios.xlsx')
                salvar_dados(df_usuarios, 'usuarios_backup.xlsx')
                print("Usuário atualizado com sucesso!")
            else:
                print("Usuário não encontrado!")
        elif escolha == '3':
            print(df_usuarios)
        elif escolha == '0':
            break
        else:
            print("Opção inválida!")

def menu_produtos():
    df_produtos, origem_produtos = carregar_dados('produtos.xlsx', 'produtos_backup.xlsx')
    while True:
        print("\nMenu Produtos")
        print("(1) Adicionar Produto")
        print("(2) Atualizar Produto")
        print("(3) Listar Produtos")
        print("(0) Voltar ao Menu Principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            nome = input("Nome do Produto: ")
            preco = float(input("Preço: "))
            novo_produto = pd.DataFrame([{'Nome': nome, 'Preço': preco}])
            df_produtos = pd.concat([df_produtos, novo_produto], ignore_index=True)
            salvar_dados(df_produtos, 'produtos.xlsx')
            if origem_produtos == 'produtos_backup.xlsx':
                sincronizar_dados(df_produtos, 'produtos.xlsx')
            salvar_dados(df_produtos, 'produtos_backup.xlsx')
            print("Produto adicionado com sucesso!")
        elif escolha == '2':
            nome = input("Nome do produto a ser atualizado: ")
            produto = df_produtos[df_produtos['Nome'] == nome]
            if not produto.empty:
                preco = float(input("Novo Preço: "))
                df_produtos.loc[df_produtos['Nome'] == nome, 'Preço'] = preco
                salvar_dados(df_produtos, 'produtos.xlsx')
                salvar_dados(df_produtos, 'produtos_backup.xlsx')
                print("Produto atualizado com sucesso!")
            else:
                print("Produto não encontrado!")
        elif escolha == '3':
            print(df_produtos)
        elif escolha == '0':
            break
        else:
            print("Opção inválida!")

def menu_pedidos():
    if not os.path.exists('pedidos.xlsx'):
        print("Estamos em manutenção, voltamos em breve")
        return

    df_pedidos = carregar_dados('pedidos.xlsx')
    while True:
        print("\nMenu Pedidos")
        print("(1) Adicionar Pedido")
        print("(2) Listar Pedidos")
        print("(0) Voltar ao Menu Principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            cliente = input("Nome do Cliente: ")
            produto = input("Nome do Produto: ")
            quantidade = int(input("Quantidade: "))
            novo_pedido = pd.DataFrame([{'Cliente': cliente, 'Produto': produto, 'Quantidade': quantidade}])
            df_pedidos = pd.concat([df_pedidos, novo_pedido], ignore_index=True)
            salvar_dados(df_pedidos, 'pedidos.xlsx')
            print("Pedido adicionado com sucesso!")
        elif escolha == '2':
            print(df_pedidos)
        elif escolha == '0':
            break
        else:
            print("Opção inválida!")

def menu_estoque():
    if not os.path.exists('estoque.xlsx'):
        print("Estamos em manutenção, voltamos em breve")
        return

    df_estoque = carregar_dados('estoque.xlsx')
    while True:
        print("\nMenu Estoque")
        print("(1) Adicionar ao Estoque")
        print("(2) Listar Estoque")
        print("(0) Voltar ao Menu Principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            produto = input("Nome do Produto: ")
            quantidade = int(input("Quantidade: "))
            produto_estoque = df_estoque[df_estoque['Produto'] == produto]
            if not produto_estoque.empty:
                df_estoque.loc[df_estoque['Produto'] == produto, 'Quantidade'] += quantidade
            else:
                novo_estoque = pd.DataFrame([{'Produto': produto, 'Quantidade': quantidade}])
                df_estoque = pd.concat([df_estoque, novo_estoque], ignore_index=True)
            salvar_dados(df_estoque, 'estoque.xlsx')
            print("Estoque atualizado com sucesso!")
        elif escolha == '2':
            print(df_estoque)
        elif escolha == '0':
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    inicializar()
    menu()
