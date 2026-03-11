import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as tb
from models import Product, Inventory


class InventoryApp:
    def __init__(self, root, username=None, role="viewer", logout_callback=None):
        self.inventory = Inventory()
        self.root = root
        self.root.title("Inventory System with Tabs")

        if username:
            tb.Label(
                root,
                text=f"Logged in as: {username} ({role})",
                bootstyle="info",
                font=("Arial", 12),
            ).pack(pady=5)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Menu Tab
        self.menu_frame = tk.Frame(self.notebook)
        self.notebook.add(self.menu_frame, text="Menu")
        tb.Label(
            self.menu_frame,
            text="📦 Inventory System",
            bootstyle="primary",
            font=("Arial", 16, "bold"),
        ).pack(pady=20)

        # Product info Tab (admin only)
        if role == "admin":
            self.input_frame = tk.Frame(self.notebook)
            self.notebook.add(self.input_frame, text="Product info page")

            tk.Label(self.input_frame, text="Item ID").grid(row=0, column=0)
            tk.Label(self.input_frame, text="Name").grid(row=1, column=0)
            tk.Label(self.input_frame, text="Price").grid(row=2, column=0)
            tk.Label(self.input_frame, text="Quantity").grid(row=3, column=0)
            tk.Label(self.input_frame, text="Category").grid(row=4, column=0)

            self.entry_id = tk.Entry(self.input_frame)
            self.entry_name = tk.Entry(self.input_frame)
            self.entry_price = tk.Entry(self.input_frame)
            self.entry_qty = tk.Entry(self.input_frame)
            self.entry_cat = tk.Entry(self.input_frame)

            self.entry_id.grid(row=0, column=1)
            self.entry_name.grid(row=1, column=1)
            self.entry_price.grid(row=2, column=1)
            self.entry_qty.grid(row=3, column=1)
            self.entry_cat.grid(row=4, column=1)

            tb.Button(
                self.input_frame,
                text="Add Product",
                bootstyle="success",
                command=self.add_product,
            ).grid(row=5, column=0, columnspan=2)
            tb.Button(
                self.input_frame,
                text="Remove Product",
                bootstyle="danger",
                command=self.remove_product,
            ).grid(row=6, column=0, columnspan=2)
            tb.Button(
                self.input_frame,
                text="Update Product",
                bootstyle="info",
                command=self.update_product,
            ).grid(row=6, column=2, columnspan=2)

        # Data dashboard Tab
        self.data_frame = tk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="Data dashboard")

        # Treeview 表格顯示產品
        self.tree = ttk.Treeview(
            self.data_frame,
            columns=("ID", "Name", "Price", "Qty", "Category"),
            show="headings",
        )
        self.tree.heading("ID", text="Item ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Qty", text="Quantity")
        self.tree.heading("Category", text="Category")
        self.tree.pack(pady=10, fill="x")

        self.frame_chart = tk.Frame(self.data_frame)
        self.frame_chart.pack(pady=10)

        self.frame_kpi = tk.Frame(self.data_frame)
        self.frame_kpi.pack(pady=10)

        tb.Button(
            self.data_frame,
            text="List Products",
            bootstyle="primary",
            command=self.list_products,
        ).pack(pady=5)
        tb.Button(
            self.data_frame,
            text="Update Dashboard",
            bootstyle="warning",
            command=self.update_dashboard,
        ).pack(pady=5)

        if logout_callback:
            tb.Button(
                root, text="Logout", bootstyle="danger", command=logout_callback
            ).pack(pady=5)

    # ---------------- 功能 ----------------
    def add_product(self):
        try:
            item_id = self.entry_id.get()
            name = self.entry_name.get()
            price = float(self.entry_price.get())
            qty = int(self.entry_qty.get())
            category = self.entry_cat.get()
            product = Product(item_id, name, price, qty, category)
            self.inventory.add_product(product)
            messagebox.showinfo("Success", f"Product {name} added!")
            self.list_products()
        except ValueError:
            messagebox.showerror("Error", "Invalid input!")

    def remove_product(self):
        item_id = self.entry_id.get()
        success = self.inventory.remove_product(item_id)
        if success:
            messagebox.showinfo("Success", f"Product {item_id} removed")
        else:
            messagebox.showerror("Error", f"Product {item_id} not found")
        self.list_products()
        self.update_dashboard()

    def update_product(self):
        try:
            item_id = self.entry_id.get()
            new_price = (
                float(self.entry_price.get()) if self.entry_price.get() else None
            )
            new_qty = int(self.entry_qty.get()) if self.entry_qty.get() else None
            success = self.inventory.update_product(item_id, new_price, new_qty)
            if success:
                messagebox.showinfo("Success", f"Product {item_id} updated")
            else:
                messagebox.showerror("Error", f"Product {item_id} not found!")
            self.list_products()
            self.update_dashboard()
        except ValueError:
            messagebox.showerror("Error", "Invalid input")

    def list_products(self):
        # 清空 Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        # 插入新資料
        products = self.inventory.list_all_products()
        for p in self.inventory._Inventory__products.values():  # 直接取 Product object
            self.tree.insert(
                "",
                "end",
                values=(p.item_id, p.name, p.price, p.get_quantity(), p.category),
            )

    def update_dashboard(self):
        # remove old chart
        for widget in self.frame_chart.winfo_children():
            widget.destroy()

        summary = self.inventory.category_summary()
        if summary:
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.pie(summary.values(), labels=summary.keys(), autopct="%1.1f%%")
            ax.set_title("Inventory Distribution by Category")
            canvas = FigureCanvasTkAgg(fig, master=self.frame_chart)
            canvas.draw()
            canvas.get_tk_widget().pack()

        # remove old KPI
        for widget in self.frame_kpi.winfo_children():
            widget.destroy()

        kpi_data = {
            "Total Quantity": self.inventory.total_quantity(),
            "Low Stock Count (<10)": self.inventory.low_stock_count(),
            "Average Price": round(self.inventory.avg_price(), 2),
            "Category Count": self.inventory.category_count(),
        }
        for k, v in kpi_data.items():
            tb.Label(
                self.frame_kpi,
                text=f"{k}: {v}",
                bootstyle="secondary",
                font=("Arial", 12, "bold"),
            ).pack()
