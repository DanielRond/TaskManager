[English](#english) | [Português](#português)

---

<a name="english"></a>

# English

## TaskManager

TaskManager is a desktop task management application developed in Python, using the Tkinter library for the graphical interface and JSON for persistent local storage.

It allows users to add, update, remove, and automatically organize daily tasks with detailed metadata such as priority level, description, creation date, and due date. TaskManager is a compact, efficient, and visually intuitive solution for keeping commitments under control.

---

## Academic Context and Project Future

Author: **Daniel Rond de Jesus dos Santos**, Bachelor of Computer Science from the Federal University of Pará (UFPA), Belém campus.\
This project was originally developed as part of the practical requirements for the **Algorithms** course, under the supervision of Professor **Paula Christina Figueira Cardoso**.

Beyond its initial academic purpose, the **TaskManager** ecosystem was designed to be modular and scalable. For this reason, the program will continue to receive updates, new features, and design improvements in the future, serving as an ongoing **personal software development project**.

---

## Tools Used

The project architecture was designed with portability and robustness in mind, using the following resources:

* **Python:** Main programming language used for the entire business logic, in-memory state handling, and flow control.
* **Tkinter (and ttk):** Native Python library for building graphical user interfaces (GUI). The app uses a modern structure divided into sub-blocks (*Frames*), hybrid layout managers (`pack` and `grid`), and dynamic event bindings (such as `<Motion>` for reading mouse cursor coordinates).
* **JSON:** Used for native data serialization and deserialization (`json.dump` and `json.loads`). It keeps saved lists and dictionaries consistent and readable for both humans and computers.
* **Pathlib:** Replaces raw string file paths. It ensures that `tasks.json` is resolved dynamically relative to the script execution root, avoiding directory issues across operating systems (Windows, Linux, macOS).

---

## Installation

Because the project uses only native packages from the Python standard library, setup is very simple and does not require complex virtual environments or external dependencies (`pip`).

### Prerequisites

Make sure Python 3 is installed on your machine. You can check it by running the following command in your terminal or command prompt:

```bash
python --version
```

### Step by Step

1. Download the project script file (for example, `main.py`).
2. Open your operating system terminal or command prompt.
3. Navigate to the folder where the file was saved:

```bash
cd /path/to/project/folder
```

4. Run the application with the command:

```bash
python main.py
```

---

## How to Use

The TaskManager interface is divided into three main modular sections: **Input Form**, **Display Panel (Listbox)**, and **Actions (Buttons)**.

### 1. Adding a Task

1. In the **Task** field, enter the title of your activity (required).
2. Select the priority level in the **Priority** selector (*High*, *Medium*, *Low*).
3. In the **Description** field, enter details or notes about the task.
4. Set the deadline in the **Due date** field. You can type it manually in `DD/MM/YYYY` format or use the quick presets in **Due preset** (1 day, 1 week, 1 month) for automatic filling.
5. Click **Add Task**. The task will be listed and automatically reordered according to priority and creation time.

### 2. Updating a Task

1. Click the desired task directly in the visual list to select it.
2. The corresponding data will remain in the upper editing fields so you can modify them.
3. Change the text, priority, or deadlines as needed.
4. Click **Update Task** to apply the changes directly in memory.

### 3. Removing a Task

1. Click the desired task in the list.
2. Press **Remove Task**. The interface will be cleared and synchronized instantly.

### 4. Saving Your Data

Changes on screen remain in volatile memory (RAM) while the program is running. To permanently save your tasks to disk before closing the program:

* Click **Save Tasks**. A confirmation message will indicate that `tasks.json` has been updated.

### 5. Clear All

If you want to clear your entire history and start from scratch:

* Click **Clear All**. The system will show a confirmation dialog asking whether you really want to perform the action. Once confirmed, memory, fields, and files will be reset in a clean and safe way.

### Interface Tip (UX)

Hover the mouse pointer over any button or `Listbox` item and pause for a second. The **Dynamic Tooltips** system will open a small floating window showing extended information (such as the full description and exact creation date) without needing to open or edit the item.

---

<a name="português"></a>

# Português

## TaskManager

TaskManager é um aplicativo de gerenciamento de tarefas desktop desenvolvido em Python, utilizando a biblioteca Tkinter para a construção de sua interface gráfica e o formato JSON para a persistência e armazenamento seguro de dados locais.

Ele permite que os usuários adicionem, atualizem, removam e organizem de forma automatizada as suas tarefas diárias com metadados detalhados, como nível de prioridade, descrição, data de criação e data de entrega. O TaskManager é a solução ideal para quem busca uma ferramenta enxuta, eficiente e visualmente intuitiva para manter seus compromissos sob controle.

---

## Contexto Acadêmico e Futuro do Projeto

Autor: **Daniel Rond de Jesus dos Santos** bacharel em Ciência da Computação pela Universidade Federal do Pará (UFPA), campus Belém.\
Este projeto foi desenvolvido originalmente como parte dos requisitos práticos da disciplina de **Algoritmos**, sob a orientação da professora **Paula Christina Figueira Cardoso**.

Além de cumprir o papel avaliativo inicial, o ecossistema do **TaskManager** foi projetado de forma modular e escalável. Por este motivo, o programa continuará a receber atualizações, novas features e melhorias de design futuramente, servindo como um **projeto pessoal contínuo** de desenvolvimento de software.

---

## Ferramentas Utilizadas

A arquitetura do projeto foi estruturada com foco em portabilidade e robustez, utilizando os seguintes recursos:

* **Python:** Linguagem de programação principal utilizada para toda a construção da lógica de negócios, manipulação de estados em memória e controle de fluxos de dados.
* **Tkinter (e ttk):** Biblioteca nativa do Python para desenvolvimento de interfaces de usuário (GUI). Foi implementada uma estrutura moderna dividida em sub-blocos (*Frames*), gerenciadores híbridos de layout (`pack` e `grid`), e binds de eventos dinâmicos (como o `<Motion>` para leitura de coordenadas do cursor do mouse).
* **JSON:** Utilizado para a serialização e desserialização de dados de forma nativa (`json.dump` e `json.loads`). Garante que a estrutura das listas e dicionários salvos permaneça consistente e legível tanto para humanos quanto para o computador.
* **Pathlib:** Substitui o uso antigo de strings cruas em caminhos de arquivos. Garante que o arquivo `tasks.json` seja resolvido de forma dinâmica de acordo com a raiz de execução do script, impedindo quebras de diretório em múltiplos sistemas operacionais (Windows, Linux, macOS).

---

## Instalação

Como o projeto utiliza apenas pacotes nativos da biblioteca padrão do Python, o processo de configuração é extremamente simples e não necessita de ambientes virtuais complexos ou instalação de dependências externas (`pip`).

### Pré-requisitos

Certifique-se de ter o Python 3 instalado em sua máquina. Você pode verificar executando no terminal ou prompt de comando:

```bash
python --version
```

### Passo a Passo

1. Baixe o arquivo contendo o script do projeto (ex: `main.py`).
2. Abra o terminal ou prompt de comando do seu sistema operacional.
3. Navegue até o diretório onde o arquivo foi salvo:

```bash
cd /caminho/ate/a/pasta/do/projeto
```

4. Execute a aplicação com o comando:

```bash
python main.py
```

---

## Como Usar

A interface do TaskManager é dividida de maneira modular em três seções principais: **Formulário de Entrada**, **Painel de Visualização (Listbox)** e **Ações (Botões)**.

### 1. Adicionando uma Tarefa

1. No campo **Task**, digite o título da sua atividade (obrigatório).
2. Selecione o nível de importância no seletor **Priority** (*High*, *Medium*, *Low*).
3. No campo **Description**, digite detalhes ou notas sobre a tarefa.
4. Defina o prazo no campo **Due date**. Você pode digitar manualmente no formato `DD/MM/YYYY` ou usar os atalhos rápidos do **Due preset** (1 dia, 1 semana, 1 mês) para autopreenchimento dinâmico.
5. Clique em **Add Task**. A tarefa será listada e reordenada automaticamente seguindo os critérios de prioridade e tempo de criação.

### 2. Atualizando uma Tarefa

1. Clique na tarefa desejada diretamente na lista visual para selecioná-la.
2. Os dados correspondentes serão mantidos nos campos de edição superiores para que você possa modificá-los.
3. Modifique o texto, a prioridade ou os prazos necessários.
4. Clique em **Update Task** para injetar as modificações diretamente na memória.

### 3. Removendo uma Tarefa

1. Clique sobre a tarefa desejada na lista.
2. Pressione o botão **Remove Task**. A interface será limpa e sincronizada instantaneamente.

### 4. Salvando seus Dados

As alterações em tela permanecem em cache volátil (RAM) enquanto o programa roda. Para salvar definitivamente suas tarefas no disco rígido antes de fechar o programa:

* Clique no botão **Save Tasks**. Uma mensagem de confirmação indicará que o arquivo `tasks.json` foi atualizado.

### 5. Limpeza Total

Se desejar limpar todo o seu histórico e começar do zero:

* Clique em **Clear All**. O sistema exibirá uma caixa de diálogo perguntando se você tem certeza de que deseja realizar a ação. Confirmando, toda a memória, campos e arquivos serão resetados de forma limpa e segura.

### Dica de Interface (UX)

Passe o ponteiro do mouse e segure-o por um segundo sobre qualquer botão ou item listado na `Listbox`. O sistema de **Tooltips Dinâmicos** abrirá uma pequena janela flutuante exibindo informações estendidas (como a descrição completa e a data exata de criação) sem que você precise abrir ou editar o item.