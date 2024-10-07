import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
import yaml
import webbrowser, os
import shutil
import threading

# Variável global para armazenar o caminho da pasta
pasta_config = None

# Carrega os dados do YAML (se existir)
try:
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        pasta_config = config.get("pasta_documentacao")
except FileNotFoundError:
    # Se o arquivo não existir, cria um novo
    config = {"pasta_documentacao": ""}
    with open("config.yaml", "w", encoding="utf-8") as f:
        yaml.dump(config, f)
    pasta_config = ""

# Cria a janela principal
janela = tk.Tk()
janela.title("Toolbox Arquitetura")
janela.geometry("400x300")

# Cria o menu
menubar = tk.Menu(janela)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Catálogo de Documentação", command=lambda: abrir_catalogo())
filemenu.add_command(label="Artefatos de Projeto", command=lambda: abrir_artefatos_projeto())
menubar.add_cascade(label="Ferramentas", menu=filemenu)

# Menu de Configuração
configmenu = tk.Menu(menubar, tearoff=0)
configmenu.add_command(label="Repositorio", command=lambda: abrir_repositorio())
configmenu.add_command(label="Atualizar Modelos", command=lambda: atualizar_repo_arch_model())
menubar.add_cascade(label="Configuração", menu=configmenu)

janela.config(menu=menubar)

# def abrir_artefatos_projeto():
#     root_folder = os.getcwd()
#     project_folder = os.path.join(root_folder, "project-repo")
#     artfact_folder = os.path.join(root_folder, "project-repo", "out")
#     os.chdir(project_folder)
#     os.system("git pull")
#     os.system("yarn build-all")
#     webbrowser.open(os.path.realpath(artfact_folder))

# Botão para salvar a configuração
def abrir_artefatos_projeto():

    # Cria uma nova janela para exibir o progresso
    janela_progresso = tk.Toplevel(janela)
    janela_progresso.title("Criando Artefatos de Projeto")
    janela_progresso.geometry("250x50")

    # Label para exibir o status
    label_status = tk.Label(janela_progresso, text="Iniciando processo...")
    label_status.pack(pady=10)

    # Função para atualizar o status na label
    def atualizar_status(texto):
        label_status.config(text=texto)

    # Executa o processo de atualização em um processo separado
    def executar_atualizacao():
        root_folder = os.getcwd()
        project_folder = os.path.join(root_folder, "project-repo")
        artfact_folder = os.path.join(root_folder, "project-repo", "out")
        try:
            if os.path.exists(project_folder):
                os.chdir(project_folder)
                atualizar_status("Atualizando projeto...")
                os.system("git pull")
                atualizar_status("Contruindo artefatos de projeto...")
                os.system("yarn build-all")
                if os.path.exists(artfact_folder):  
                    atualizar_status("Concluido ...")
                    webbrowser.open(os.path.realpath(artfact_folder))

            # Imprime o valor do campo no terminal
            # atualizar_status("Instalando dependências...")
            # print(f"URL do repositório: {pasta_config}")
            # os.system(f'git clone {pasta_config} project-repo')
            # os.chdir(project_repo_path)
            # os.system("yarn setup")
            # os.chdir(root_folder)
            os.chdir(root_folder)
        except OSError as e:
            os.chdir(root_folder)
            print("Error: %s - %s." % (e.filename, e.strerror))

        # Fecha a janela de progresso após a conclusão
        janela_progresso.destroy()

    # Inicia a atualização em um novo thread
    executa_atualizacao = threading.Thread(target=executar_atualizacao)
    executa_atualizacao.start()


# Função para abrir a janela do catálogo
def abrir_catalogo():
    # Limpa a janela, exceto o menu
    for widget in janela.winfo_children():
        if widget != menubar:
            widget.destroy()

    # Cria a frame para a lista de documentos
    frame_catalogo = tk.Frame(janela)
    frame_catalogo.pack(pady=10)

    # Cria a árvore de itens
    tree = ttk.Treeview(frame_catalogo, columns=("name", "description"), show="headings")
    tree.heading("name", text="Nome")
    tree.heading("description", text="Descrição")

    # Busca modelos no repo pai
    root_folder = os.getcwd()
    repo_path = os.path.join(root_folder, "arch-model-repo")
    file_path = os.path.join(repo_path, "toolbox", "doc-catalog", "files.yaml")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            documentacao = yaml.safe_load(f)
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo 'files.yaml' não encontrado em doc-catalog.")
        return

    # Insere os itens na árvore
    for item in documentacao:
        tree.insert("", tk.END, values=(item["name"], item["description"], item["path"]))

    # Função para abrir a janela de detalhes
    def abrir_detalhes(event):
        item_selecionado = tree.selection()[0]
        item_dados = tree.item(item_selecionado, "values")
        nome = item_dados[0]
        descricao = item_dados[1]
        caminho_item = item_dados[2]

        # Cria a janela de detalhes
        janela_detalhes = tk.Toplevel(janela)
        janela_detalhes.title(f"Detalhes de {nome}")

        # Label para o nome do documento
        label_nome = tk.Label(janela_detalhes, text=f"Nome: {nome}")
        label_nome.pack(pady=5)

        # Label para a descrição do documento
        label_descricao = tk.Label(janela_detalhes, text=f"Descrição: {descricao}")
        label_descricao.pack(pady=5)

        # Botões de ação
        def salvar_markdown():
            pasta_destino = filedialog.askdirectory()
            if pasta_destino:
                try:
                    # Copia o arquivo para a pasta de destino
                    arquivo_origem = os.path.join(repo_path, "toolbox", "doc-catalog", caminho_item[1:])
                    caminho_completo = os.path.join(pasta_destino, caminho_item[6:])
                    shutil.copy2(arquivo_origem, caminho_completo)
                    messagebox.showinfo("Sucesso", f"Arquivo {nome}.md salvo em {pasta_destino}")
                    janela_detalhes.destroy()
                except FileNotFoundError:
                    messagebox.showerror("Erro", f"Arquivo '{nome}.md' não encontrado.")
                except shutil.Error as e:
                    messagebox.showerror("Erro", f"Erro ao copiar arquivo: {e}")

        def cancelar():
            janela_detalhes.destroy()

        salvar_markdown_button = tk.Button(janela_detalhes, text="Salvar Markdown", command=salvar_markdown)
        salvar_markdown_button.pack(pady=10)

        cancelar_button = tk.Button(janela_detalhes, text="Cancelar", command=cancelar)
        cancelar_button.pack(pady=10)

    # Liga o evento de clique duplo na árvore à função abrir_detalhes
    tree.bind("<Double-1>", abrir_detalhes)

    # Adiciona o título e a descrição
    titulo = tk.Label(frame_catalogo, text="Catálogo de Documentação", font=("Arial", 16, "bold"))
    titulo.pack(pady=10)
    descricao = tk.Label(frame_catalogo, text="Lista de documentos disponíveis:")
    descricao.pack()

    # Adiciona a árvore à frame
    tree.pack(pady=10)

    # Adiciona a frame à janela
    frame_catalogo.pack()

# Função para abrir a janela de repositório
def abrir_repositorio():
    # Cria a janela de configuração
    janela_config = tk.Toplevel(janela)
    janela_config.title("Configuração do Repositório")

    # Label para o caminho da pasta
    label_pasta = tk.Label(janela_config, text="URL do Repositório:")
    label_pasta.pack(pady=5)

    # Entry para o caminho da pasta
    entry_pasta = tk.Entry(janela_config, width=50)
    entry_pasta.pack(pady=5)
    entry_pasta.insert(0, pasta_config)

    # Botão para salvar a configuração
    def pegar_repo_projeto():
        # Cria uma nova janela para exibir o progresso
        janela_progresso = tk.Toplevel(janela)
        janela_progresso.title("Atualizando Catálogo")
        janela_progresso.geometry("250x50")


        # Label para exibir o status
        label_status = tk.Label(janela_progresso, text="Iniciando busca...")
        label_status.pack(pady=10)

        # Função para atualizar o status na label
        def atualizar_status(texto):
            label_status.config(text=texto)

        # Executa o processo de atualização em um processo separado
        def executar_atualizacao():
            global pasta_config
            root_folder = os.getcwd()
            project_repo_path = os.path.join(os.getcwd(), "project-repo")

            try:
                if os.path.exists(project_repo_path):
                    os.system("node ./clean.js")
                    # for caminho, pastas, arquivos in os.walk(project_repo_path):
                    #     for pasta in pastas[:]:
                    #         pastas.remove(pasta)
                    #         shutil.rmtree(os.path.join(caminho, pasta))


                pasta_config = entry_pasta.get()
                janela_config.destroy()

                config = {"pasta_documentacao": pasta_config}
                with open("config.yaml", "w", encoding="utf-8") as f:
                    yaml.dump(config, f)

                # Imprime o valor do campo no terminal
                atualizar_status("Instalando dependências...")
                print(f"URL do repositório: {pasta_config}")
                os.system(f'git clone {pasta_config} project-repo')
                os.chdir(project_repo_path)
                os.system("yarn setup")
                os.chdir(root_folder)
            except OSError as e:
                os.chdir(root_folder)
                print("Error: %s - %s." % (e.filename, e.strerror))

            # Fecha a janela de progresso após a conclusão
            janela_progresso.destroy()

        # Inicia a atualização em um novo thread
        executa_atualizacao = threading.Thread(target=executar_atualizacao)
        executa_atualizacao.start()

    button_salvar = tk.Button(janela_config, text="Salvar", command=pegar_repo_projeto)
    button_salvar.pack(pady=5)


# Função para atualizar o catálogo
def atualizar_repo_arch_model():
    # Cria uma nova janela para exibir o progresso
    janela_progresso = tk.Toplevel(janela)
    janela_progresso.title("Atualizando Catálogo")
    janela_progresso.geometry("250x50")


    # Label para exibir o status
    label_status = tk.Label(janela_progresso, text="Iniciando atualização...")
    label_status.pack(pady=10)

    # Função para atualizar o status na label
    def atualizar_status(texto):
        label_status.config(text=texto)

    # Executa o processo de atualização em um processo separado
    def executar_atualizacao():
        root_folder = os.getcwd()
        repo_path = os.path.join(root_folder, "arch-model-repo")

        if not os.path.exists(repo_path):
            atualizar_status("Clonando repositório...")
            os.system("git clone https://github.com/fulviocoelho/arch-model-repo.git")
            atualizar_status("Instalando dependências...")
            os.chdir(repo_path)
            os.system("npm install -g yarn")
            os.system("yarn")
            atualizar_status("Configurando repositório...")
            os.system("yarn setup")
            atualizar_status("Atualização concluída!")
            os.chdir(root_folder)
        else:
            atualizar_status("Atualizando repositório...")
            os.chdir(repo_path)
            os.system("npm install -g yarn")
            os.system("yarn update")
            atualizar_status("Atualização concluída!")
            os.chdir(root_folder)

        # Fecha a janela de progresso após a conclusão
        janela_progresso.destroy()

    # Inicia a atualização em um novo thread
    executa_atualizacao = threading.Thread(target=executar_atualizacao)
    executa_atualizacao.start()

# Inicia a aplicação
janela.mainloop()