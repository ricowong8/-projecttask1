# Inventory Management System (OOP + GUI)

This project is an **Object-Oriented Programming (OOP)** based application designed to simulate a real-life inventory management system.  
It demonstrates the use of core OOP concepts and provides a graphical user interface (GUI) for product entry, data visualization, and dashboard reporting.

---

## 📂 Project Structure

Defined in 3 parts, app.py, model.py, gui.py. Each of the python file will contained the different parts. 

---

## 📝 Features

- **OOP Concepts**
  - **Abstraction**: `Item` is an abstract class.
  - **Inheritance**: `Product` inherits from `Item`.
  - **Encapsulation**: Private attributes (e.g., `__quantity`) with controlled access.
  - **Polymorphism**: Overridden methods such as `get_info()`.

- **System Functions**
  - Add new products
  - Remove products
  - Search products
  - Display product list
  - Dashboard with Pie Chart and KPI metrics

- **GUI**
  - Built with Tkinter Notebook, divided into three tabs:
    1. **Menu Page** – System overview
    2. **Product Entry Page** – Input product details
    3. **Data View Page** – Display product list and dashboard

---

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/username/inventory-system.git
cd inventory-system

🚀 Usage
Run the main application:

The system will launch a GUI with three tabs for navigation.
---
📊 Dashboard Example
• Pie Chart: Shows inventory distribution by category
• KPI Metrics:
	◦ Total Quantity
	◦ Low Stock Count (<10)
	◦ Average Price
	◦ Category Count

📝 Notes
• This project is part of COMP2090SEF Group Project / COMP8090SEF Individual Project.
• If extended from a previous course project, the final report must declare the source and demonstrate ≥60% new content compared to the earlier submission.

📜 License
MIT License
---

This README clearly explains the **project purpose, structure, features, installation, usage, and dashboard outputs**.  