import csv
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry('800x500')
        self.initialize_ui()

    def initialize_ui(self):

        self.title("Учет расходов")
        self.grid_rowconfigure(7, minsize=100, weight=1)
        self.grid_columnconfigure(2, minsize=100, weight=1)

        # Create entry and label for date
        self.date_label = tk.Label(self, text="Дата (ДД.ММ.ГГГГ):")
        self.date_entry = tk.Entry(self, width=40)
        self.date_label.grid(row=0, column=0, sticky='w', padx=5, pady=10)
        self.date_entry.grid(row=0, column=1, sticky="e", padx=5, pady=10)

        # Create entry and label for Category
        self.cat_label = tk.Label(self, text="Категория:")
        self.cat_entry = tk.Entry(self, width=40)
        self.cat_label.grid(row=1, column=0, sticky='w', padx=5, pady=10)
        self.cat_entry.grid(row=1, column=1, sticky='e', padx=5, pady=10)

        # Create entry and label for amount
        self.amount_label = tk.Label(self, text="Сумма:")
        self.vcmd = self.register(self.validate)
        self.amount_entry = tk.Entry(self, validate="key", validatecommand=(self.vcmd, '%P'), width=40)
        self.amount_label.grid(row=2, column=0, sticky='w', padx=5, pady=10)
        self.amount_entry.grid(row=2, column=1, sticky='e', padx=5, pady=10)

        # Create button for adding entries in table
        self.submit_button = tk.Button(self, text="Добавить", command=self.add_expense)
        self.submit_button.grid(row=3, column=1, sticky='n', padx=5, pady=25)

        # Create button for deleting selected items from table
        self.delete_button = tk.Button(self, text="Удалить", command=self.delete_selected_items)
        self.delete_button.grid(row=8, column=1, sticky='n', padx=5, pady=25)

        # Labels for outputting summ
        self.sum_label = tk.Label(self, text="Общая сумма расходов:")
        self.sum_label_output = tk.Label(self, text=str(0.0))
        self.sum_label.grid(row=9, column=0, sticky=tk.W, padx=5, pady=10)
        self.sum_label_output.grid(row=9, column=1, sticky='e', padx=5, pady=10)

        # Create save and open menu
        self.s_var = tk.StringVar()
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.file_menu = tk.Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Save file", command=self.save_file)
        self.file_menu.add_command(label="Open file", command=self.load_from_file)

        # Create treeview
        columns = ('Date', 'Category', 'Amount')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.heading('Date', text='Дата')
        self.tree.heading("Category", text="Категория")
        self.tree.heading('Amount', text='Сумма')
        self.tree.grid(row=7, column=1, sticky=tk.W)

    def add_expense(self):
        date = self.date_entry.get()
        category = self.cat_entry.get()
        amount = self.amount_entry.get()
        self.tree.insert("", "end", values=(date, category, amount))
        self.date_entry.delete(0, "end")
        self.cat_entry.delete(0, "end")
        self.amount_entry.delete(0, "end")
        self.update_total_expenses()

    def delete_selected_items(self):
        for selected_item in self.tree.selection():
            self.tree.delete(selected_item)
        self.update_total_expenses()

    def load_from_file(self):
        file_name = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not file_name:
            return
        self.tree.delete(*self.tree.get_children())
        with open(file_name, "r") as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                self.tree.insert("", "end", values=row)
        self.update_total_expenses()

    def save_file(self):
        file_name = filedialog.asksaveasfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])

        if not file_name:
            return
        with open(file_name, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount"])
            for row in self.tree.get_children():
                writer.writerow(self.tree.item(row)['values'])

    def update_total_expenses(self):
        total = 0
        for child in self.tree.get_children():
            total += float(self.tree.item(child, 'values')[2])
        self.sum_label_output.config(text=str(total))

    def validate(self, new_text: str):
        if not new_text:  # the field is being cleared
            self.entered_number = 0
            return True
        try:
            self.entered_number = int(new_text)
            return True
        except ValueError:
            return False


if __name__ == '__main__':
    app = App()
    app.mainloop()
