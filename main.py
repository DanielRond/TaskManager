# Importação das bibliotecas usadas no programa.
import json
import tkinter as tk
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import messagebox, ttk

# Criando uma constante para o caminho do arquivo de tarefas.
TASKS_FILE = Path(__file__).resolve().with_name("tasks.json")

# Mantemos a fonte de verdade em memória para facilitar ordenação, atualização e persistência.
task_records: list[dict] = []

# Classe auxiliar para tooltip em widgets e itens da Listbox.
class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.label = None

    def show(self, text, x, y):
        if not text:
            return

        if self.tipwindow is None:
            self.tipwindow = tk.Toplevel(self.widget)
            self.tipwindow.wm_overrideredirect(True)
            try:
                self.tipwindow.attributes("-topmost", True)
            except tk.TclError:
                pass

            self.label = tk.Label(
                self.tipwindow,
                text=text,
                justify="left",
                background="#ffffe0",
                relief="solid",
                borderwidth=1,
                padx=6,
                pady=4,
                wraplength=280,
            )
            self.label.pack()
        else:
            self.label.config(text=text)

        self.tipwindow.geometry(f"+{x}+{y}")

    def hide(self):
        if self.tipwindow is not None:
            self.tipwindow.destroy()
            self.tipwindow = None
            self.label = None


# Tooltip simples para botões e campos.
def bind_widget_tooltip(widget, text):
    tooltip = ToolTip(widget)

    def on_enter(event):
        tooltip.show(text, event.x_root + 15, event.y_root + 15)

    def on_leave(_event):
        tooltip.hide()

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


# Tooltip dinâmico para cada item da Listbox.
def bind_listbox_tooltip(listbox, text_provider):
    tooltip = ToolTip(listbox)

    def on_motion(event):
        index = listbox.nearest(event.y)
        if index < 0 or index >= listbox.size():
            tooltip.hide()
            return

        if listbox.bbox(index) is None:
            tooltip.hide()
            return

        text = text_provider(index)
        if text:
            tooltip.show(text, event.x_root + 15, event.y_root + 15)
        else:
            tooltip.hide()

    def on_leave(_event):
        tooltip.hide()

    listbox.bind("<Motion>", on_motion)
    listbox.bind("<Leave>", on_leave)


# Permite que a prioridade seja convertida em um peso numérico para ordenação.
def get_priority_weight(priority):
    weights = {"high": 1, "medium": 2, "low": 3}
    return weights.get(priority.strip().lower(), 4)


# Permite que a data de criação seja convertida em um objeto datetime para ordenação.
def parse_creation_datetime(value):
    try:
        return datetime.strptime(value, "%d/%m/%Y %H:%M:%S")
    except (TypeError, ValueError):
        return datetime.min


# formata a exibição da tarefa na Listbox, incluindo prioridade e data de entrega.
def format_task_display(task):
    title = task.get("task", "").strip()
    priority = task.get("priority", "Low")
    due_date = task.get("due_date", "").strip()

    display_text = f"[{priority}] {title}"
    if due_date:
        display_text += f"  •  Due: {due_date}"
    return display_text


# formata o tooltip detalhado da tarefa, incluindo descrição, data de criação e data de entrega.
def format_task_tooltip(task):
    lines = [
        f"Task: {task.get('task', '').strip()}",
        f"Priority: {task.get('priority', 'Low')}",
    ]

    description = task.get("description", "").strip()
    if description:
        lines.append(f"Description: {description}")

    creation_date = task.get("creation_date", "").strip()
    if creation_date:
        lines.append(f"Created at: {creation_date}")

    due_date = task.get("due_date", "").strip()
    if due_date:
        lines.append(f"Due date: {due_date}")

    return "\n".join(lines)


# Atualiza a Listbox com a lista de tarefas ordenada por prioridade e data de criação.
def refresh_order():
    task_records.sort(
        key=lambda item: (
            get_priority_weight(task.get("priority", "")),
            parse_creation_datetime(task.get("creation_date", "")),
        )
    )

    list_task.delete(0, tk.END)
    for task in task_records:
        list_task.insert(tk.END, format_task_display(task))

# Calcula a data de entrega com base no atalho selecionado.
def calculate_due_date_from_preset(preset):
    if preset == "1 day":
        delta = timedelta(days=1)
    elif preset == "1 week":
        delta = timedelta(weeks=1)
    elif preset == "1 month":
        delta = timedelta(days=30)  # aproximação simples com timedelta
    else:
        return ""

    return (datetime.now() + delta).strftime("%d/%m/%Y")


# Aplica o atalho de data de entrega selecionado, preenchendo automaticamente o campo de data.
def apply_due_date_preset(_event=None):
    preset = combo_due_preset.get()
    if preset in {"1 day", "1 week", "1 month"}:
        entry_due_date.delete(0, tk.END)
        entry_due_date.insert(0, calculate_due_date_from_preset(preset))


# Função para obter o texto da descrição, garantindo que seja limpo de espaços em branco.
def get_description_text():
    return text_description.get("1.0", tk.END).strip()


# Função para obter o valor da data de entrega, validando o formato e aplicando o atalho se necessário.
def get_due_date_value():
    preset = combo_due_preset.get()
    due_date = entry_due_date.get().strip()

    if not due_date and preset in {"1 day", "1 week", "1 month"}:
        due_date = calculate_due_date_from_preset(preset)
        entry_due_date.delete(0, tk.END)
        entry_due_date.insert(0, due_date)

    if not due_date:
        messagebox.showwarning("Alert", "Please choose or type a due date!")
        return None

    try:
        datetime.strptime(due_date, "%d/%m/%Y")
    except ValueError:
        messagebox.showwarning("Alert", "Use DD/MM/YYYY for the due date!")
        return None

    return due_date


# Coleta os dados do formulário, validando entradas e retornando um dicionário estruturado da tarefa.
def collect_task_from_form(existing_task=None):
    task_title = entry_task.get().strip()
    if not task_title:
        messagebox.showwarning("Alert", "Please enter a task!")
        return None

    due_date = get_due_date_value()
    if due_date is None:
        return None

    creation_date = ""
    if existing_task:
        creation_date = existing_task.get("creation_date", "").strip()

    if not creation_date:
        creation_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Payload estruturado, com descrição, timestamp e data de entrega.
    return {
        "task": task_title,
        "priority": combo_priority.get(),
        "description": get_description_text(),
        "creation_date": creation_date,
        "due_date": due_date,
    }


# Função para limpar os campos de entrada do formulário, preparando para uma nova tarefa.
def clear_task_inputs():
    entry_task.delete(0, tk.END)
    text_description.delete("1.0", tk.END)


# Função para adicionar uma nova tarefa à lista, coletando dados do formulário e atualizando a Listbox.
def add_task():
    task = collect_task_from_form()
    if task is None:
        return

    task_records.append(task)
    clear_task_inputs()
    refresh_order()


# Função para remover a tarefa selecionada da lista, com verificação de seleção e atualização da Listbox.
def remove_task():
    selected_task = list_task.curselection()
    if not selected_task:
        messagebox.showwarning("Alert", "Please select a task to remove!")
        return

    task_index = selected_task[0]
    if 0 <= task_index < len(task_records):
        task_records.pop(task_index)

    list_task.selection_clear(0, tk.END)
    refresh_order()


# Função para atualizar a tarefa selecionada, coletando dados do formulário e mantendo a lista ordenada.
def update_task():
    selected_task = list_task.curselection()
    if not selected_task:
        messagebox.showwarning("Alert", "Please select a task to update!")
        return

    task_index = selected_task[0]
    if not (0 <= task_index < len(task_records)):
        return

    updated_task = collect_task_from_form(existing_task=task_records[task_index])
    if updated_task is None:
        return

    task_records[task_index] = updated_task
    clear_task_inputs()
    list_task.selection_clear(0, tk.END)
    refresh_order()


# Função para salvar a lista de tarefas em um arquivo JSON, garantindo persistência entre sessões.
def save_tasks():
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(task_records, f, ensure_ascii=False, indent=2)
    messagebox.showinfo("Info", "Tasks saved successfully!")


# Função para limpar todas as tarefas da lista, com confirmação do usuário e atualização da Listbox.
def clear_all_tasks():
    if not task_records:
        messagebox.showwarning("Alert", "No tasks to clear!")
        return

    response = messagebox.askyesno("Confirm", "Are you sure you want to clear all tasks?")
    if not response:
        return

    task_records.clear()
    list_task.delete(0, tk.END)
    list_task.selection_clear(0, tk.END)
    entry_task.delete(0, tk.END)
    text_description.delete("1.0", tk.END)
    entry_due_date.delete(0, tk.END)
    combo_priority.current(0)
    combo_due_preset.current(0)
    messagebox.showinfo("Info", "All tasks cleared!")


# Função para normalizar os dados carregados do arquivo JSON, garantindo consistência e preenchendo campos ausentes.
def normalize_loaded_task(item):
    if isinstance(item, dict):
        title = str(item.get("task") or item.get("task") or item.get("title") or "").strip()
        priority = str(item.get("priority") or item.get("priority") or "Low").strip() or "Low"
        description = str(item.get("description") or item.get("description") or "").strip()
        creation_date = str(item.get("creation_date") or item.get("creation_date") or "").strip()
        due_date = str(item.get("due_date") or item.get("due_date") or "").strip()

        if not creation_date:
            creation_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        if not title:
            return None

        return {
            "task": title,
            "priority": priority,
            "description": description,
            "creation_date": creation_date,
            "due_date": due_date,
        }

    if isinstance(item, str):
        text = item.strip()
        priority = "Low"
        title = text

        if text.startswith("[") and "]" in text:
            priority = text[1:text.index("]")].strip() or "Low"
            title = text[text.index("]") + 1 :].strip()

        if not title:
            return None

        return {
            "task": title,
            "priority": priority,
            "description": "",
            "creation_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "due_date": "",
        }

    return None


# Função para carregar as tarefas do arquivo JSON, tratando erros de leitura e formato, e atualizando a Listbox.
def load_tasks():
    task_records.clear()

    if not TASKS_FILE.exists():
        return

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            raw_content = f.read().strip()

        if not raw_content:
            return

        tasks = json.loads(raw_content)
        if not isinstance(tasks, list):
            raise ValueError("Invalid tasks file format")

        for item in tasks:
            task = normalize_loaded_task(item)
            if task is not None:
                task_records.append(task)

        refresh_order()
    except json.JSONDecodeError:
        messagebox.showwarning(
            "Alert",
            "tasks.json is empty or invalid. Starting with an empty task list.",
        )
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    except OSError as exc:
        messagebox.showerror("Error", f"Could not load tasks file: {exc}")
    except ValueError:
        messagebox.showwarning(
            "Alert",
            "tasks.json format is invalid. Starting with an empty task list.",
        )


# Configuração da janela principal do aplicativo, incluindo título, tamanho e restrições de redimensionamento.
root = tk.Tk()
root.title("Task Manager")
root.geometry("600x650")
root.resizable(False, False)

# Estrutura em frames para manter a UI organizada.
form_frame = tk.Frame(root)
form_frame.pack(fill="x", padx=10, pady=10)
form_frame.columnconfigure(1, weight=1)

tk.Label(form_frame, text="Task").grid(row=0, column=0, sticky="w", pady=4)
entry_task = tk.Entry(form_frame, width=45)
entry_task.grid(row=0, column=1, sticky="ew", pady=4)

tk.Label(form_frame, text="Priority").grid(row=1, column=0, sticky="w", pady=4)
priorities = ["High", "Medium", "Low"]
combo_priority = ttk.Combobox(form_frame, values=priorities, state="readonly")
combo_priority.current(0)
combo_priority.grid(row=1, column=1, sticky="ew", pady=4)

tk.Label(form_frame, text="Description").grid(row=2, column=0, sticky="nw", pady=4)
# Campo de descrição detalhada em múltiplas linhas.
text_description = tk.Text(form_frame, height=4, width=35)
text_description.grid(row=2, column=1, sticky="ew", pady=4)

tk.Label(form_frame, text="Due preset").grid(row=3, column=0, sticky="w", pady=4)
due_presets = ["Custom", "1 day", "1 week", "1 month"]
combo_due_preset = ttk.Combobox(form_frame, values=due_presets, state="readonly")
combo_due_preset.current(0)
combo_due_preset.grid(row=3, column=1, sticky="ew", pady=4)
combo_due_preset.bind("<<ComboboxSelected>>", apply_due_date_preset)

tk.Label(form_frame, text="Due date (DD/MM/YYYY)").grid(row=4, column=0, sticky="w", pady=4)
entry_due_date = tk.Entry(form_frame, width=45)
entry_due_date.grid(row=4, column=1, sticky="ew", pady=4)

# Listbox com Scrollbar para suportar listas maiores.
list_frame = tk.Frame(root)
list_frame.pack(fill="both", expand=True, padx=10, pady=10)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_task = tk.Listbox(list_frame, height=14, width=80, yscrollcommand=scrollbar.set)
list_task.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_task.yview)

# Botões organizados em grid.
button_frame = tk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=10)

btn_add = tk.Button(button_frame, text="Add Task", command=add_task, width=18)
btn_add.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

btn_update = tk.Button(button_frame, text="Update Task", command=update_task, width=18)
btn_update.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

btn_remove = tk.Button(button_frame, text="Remove Task", command=remove_task, width=18)
btn_remove.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

btn_save = tk.Button(button_frame, text="Save Tasks", command=save_tasks, width=18)
btn_save.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

btn_clear = tk.Button(button_frame, text="Clear All", command=clear_all_tasks, width=38)
btn_clear.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

button_frame.columnconfigure(0, weight=1)
button_frame.columnconfigure(1, weight=1)

# Tooltips nos botões e na lista.
bind_widget_tooltip(btn_add, "Add a new task with description, timestamp and due date.")
bind_widget_tooltip(btn_update, "Update the selected task and keep the list automatically ordered.")
bind_widget_tooltip(btn_remove, "Remove the selected task from the list.")
bind_widget_tooltip(btn_save, "Save the current tasks to tasks.json.")
bind_widget_tooltip(btn_clear, "Clear all tasks after confirmation.")
bind_widget_tooltip(combo_due_preset, "Quick due date options automatically fill the date field.")

# Função nomeada para o tooltip da Listbox, evitando lambda anônimo.
def get_listbox_tooltip_text(index: int) -> str:
    for current_index, task in enumerate(task_records):
        if current_index == index:
            return format_task_tooltip(task)
    return ""

bind_listbox_tooltip(list_task, get_listbox_tooltip_text)

load_tasks()

root.mainloop()