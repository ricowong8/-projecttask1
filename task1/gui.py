import matplotlib

matplotlib.use("QtAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QFormLayout,
    QStatusBar,
    QHeaderView,
    QScrollArea,
    QFrame,
    QSizePolicy,
)
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt, Signal

from models import Product, Inventory


# ──────────────────────────────────────────────
# KPI 卡片
# ──────────────────────────────────────────────
class KpiCard(QFrame):
    def __init__(self, title: str, value: str = "—", color: str = "#4a90d9"):
        super().__init__()
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedSize(180, 80)
        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: #2c2c2c;
                border: 1px solid {color};
                border-radius: 8px;
            }}
        """
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)

        self._title = QLabel(title)
        self._title.setStyleSheet("color: #aaaaaa; font-size: 11px;")
        self._title.setAlignment(Qt.AlignCenter)

        self._value = QLabel(value)
        self._value.setStyleSheet(
            f"color: {color}; font-size: 20px; font-weight: bold;"
        )
        self._value.setAlignment(Qt.AlignCenter)

        layout.addWidget(self._title)
        layout.addWidget(self._value)

    def update_value(self, value: str):
        self._value.setText(value)


# ──────────────────────────────────────────────
# 主視窗
# ──────────────────────────────────────────────
class InventoryApp(QMainWindow):
    logout_requested = Signal()

    def __init__(self, username: str = None, role: str = "viewer"):
        super().__init__()
        self.inventory = Inventory()
        self.role = role
        self.chart_canvas = None

        self.setWindowTitle("📦 Inventory Management System")
        self.resize(1100, 750)
        self._apply_dark_theme()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(10, 10, 10, 10)

        # Top bar
        top_bar = QHBoxLayout()
        if username:
            lbl = QLabel(f"👤  {username}  |  Role: {role.upper()}")
            lbl.setStyleSheet("color: #64b5f6; font-size: 13px; font-weight: bold;")
            top_bar.addWidget(lbl)
        top_bar.addStretch()

        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setStyleSheet(
            "background:#c0392b; color:white; padding:4px 12px; border-radius:4px;"
        )
        logout_btn.clicked.connect(self.logout_requested.emit)
        top_bar.addWidget(logout_btn)
        root.addLayout(top_bar)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            """
            QTabBar::tab          { padding: 8px 20px; font-size: 13px; }
            QTabBar::tab:selected { background: #3a3a3a; color: #64b5f6; }
        """
        )
        root.addWidget(self.tabs)

        self._build_menu_tab()
        if role == "admin":
            self._build_product_tab()
        self._build_dashboard_tab()

    # ── 深色主題 ──────────────────────────────
    def _apply_dark_theme(self):
        palette = QPalette()
        for role, color in {
            QPalette.Window: QColor(28, 28, 28),
            QPalette.WindowText: QColor(220, 220, 220),
            QPalette.Base: QColor(22, 22, 22),
            QPalette.AlternateBase: QColor(35, 35, 35),
            QPalette.Text: QColor(220, 220, 220),
            QPalette.Button: QColor(55, 55, 55),
            QPalette.ButtonText: QColor(220, 220, 220),
            QPalette.Highlight: QColor(100, 150, 200),
            QPalette.HighlightedText: QColor(255, 255, 255),
        }.items():
            palette.setColor(role, color)
        self.setPalette(palette)

    # ── Tab 1：歡迎頁 ─────────────────────────
    def _build_menu_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("📦 Inventory Management System")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color: #64b5f6;")
        title.setAlignment(Qt.AlignCenter)

        sub = QLabel("Use the tabs above to manage products and view the dashboard.")
        sub.setStyleSheet("color: #aaaaaa; font-size: 13px;")
        sub.setAlignment(Qt.AlignCenter)

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(sub)
        self.tabs.addTab(tab, "🏠 Menu")

    # ── Tab 2：產品管理（Admin Only）─────────
    def _build_product_tab(self):
        tab = QWidget()
        outer = QVBoxLayout(tab)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        form = QFormLayout(content)
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(12)
        form.setContentsMargins(40, 20, 40, 20)

        def _entry(placeholder=""):
            e = QLineEdit()
            e.setPlaceholderText(placeholder)
            e.setStyleSheet(
                "background:#2a2a2a; color:#ddd; border:1px solid #555;"
                "border-radius:4px; padding:5px;"
            )
            return e

        self.entry_id = _entry("e.g. P001")
        self.entry_name = _entry("e.g. Apple")
        self.entry_price = _entry("e.g. 9.99")
        self.entry_qty = _entry("e.g. 50")
        self.entry_cat = _entry("e.g. Fruit")

        for label, widget in [
            ("Item ID:", self.entry_id),
            ("Name:", self.entry_name),
            ("Price:", self.entry_price),
            ("Quantity:", self.entry_qty),
            ("Category:", self.entry_cat),
        ]:
            form.addRow(label, widget)

        btn_row = QHBoxLayout()
        for text, color, slot in [
            ("➕  Add", "#27ae60", self.add_product),
            ("🗑  Remove", "#c0392b", self.remove_product),
            ("✏️  Update", "#2980b9", self.update_product),
            ("🧹  Clear", "#555555", self._clear_entries),
        ]:
            btn = QPushButton(text)
            btn.setStyleSheet(
                f"background:{color}; color:white; padding:8px 18px;"
                "border-radius:5px; font-size:13px;"
            )
            btn.clicked.connect(slot)
            btn_row.addWidget(btn)

        form.addRow(btn_row)
        scroll.setWidget(content)
        outer.addWidget(scroll)
        self.tabs.addTab(tab, "🛠 Product Info")

    # ── Tab 3：儀表板 ─────────────────────────
    def _build_dashboard_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Price", "Qty", "Category"])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.table, stretch=3)

        # KPI 列
        kpi_row = QHBoxLayout()
        kpi_row.setAlignment(Qt.AlignCenter)
        self.kpi_total_qty = KpiCard("Total Quantity", "—", "#64b5f6")
        self.kpi_low_stock = KpiCard("Low Stock (<10)", "—", "#e74c3c")
        self.kpi_avg_price = KpiCard("Avg Price", "—", "#2ecc71")
        self.kpi_cat_count = KpiCard("Categories", "—", "#f39c12")
        for card in [
            self.kpi_total_qty,
            self.kpi_low_stock,
            self.kpi_avg_price,
            self.kpi_cat_count,
        ]:
            kpi_row.addWidget(card)
        layout.addLayout(kpi_row)

        # 圖表區
        self.chart_frame = QWidget()
        self.chart_frame.setMinimumHeight(280)
        self.chart_frame.setLayout(QVBoxLayout())
        self.chart_frame.layout().setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.chart_frame, stretch=2)

        # 按鈕列
        btn_row = QHBoxLayout()
        for text, color, slot in [
            ("📋  List Products", "#2980b9", self.list_products),
            ("📊  Update Dashboard", "#8e44ad", self.update_dashboard),
        ]:
            btn = QPushButton(text)
            btn.setStyleSheet(
                f"background:{color}; color:white; padding:8px 22px;"
                "border-radius:5px; font-size:13px;"
            )
            btn.clicked.connect(slot)
            btn_row.addWidget(btn)
        layout.addLayout(btn_row)

        self.tabs.addTab(tab, "📊 Data Dashboard")

    # ──────────────────────────────────────────
    # 功能方法
    # ──────────────────────────────────────────
    def _clear_entries(self):
        for e in [
            self.entry_id,
            self.entry_name,
            self.entry_price,
            self.entry_qty,
            self.entry_cat,
        ]:
            e.clear()

    def _status(self, msg: str, ms: int = 3000):
        self.status_bar.showMessage(msg, ms)

    def add_product(self):
        try:
            p = Product(
                self.entry_id.text().strip(),
                self.entry_name.text().strip(),
                float(self.entry_price.text()),
                int(self.entry_qty.text()),
                self.entry_cat.text().strip(),
            )
            if self.inventory.add_product(p):
                self._status(f"✅ '{p.name}' added.")
                self._clear_entries()
                self.list_products()
                self.update_dashboard()
            else:
                QMessageBox.warning(
                    self, "Duplicate ID", f"Product ID '{p.item_id}' already exists."
                )
        except ValueError:
            QMessageBox.critical(
                self,
                "Input Error",
                "Price must be a number, Quantity must be an integer.",
            )

    def remove_product(self):
        item_id = self.entry_id.text().strip()
        if not item_id:
            QMessageBox.warning(self, "Missing ID", "Please enter an Item ID.")
            return
        confirm = QMessageBox.question(
            self,
            "Confirm Remove",
            f"Remove product '{item_id}'?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if confirm == QMessageBox.Yes:
            if self.inventory.remove_product(item_id):
                self._status(f"🗑 '{item_id}' removed.")
                self._clear_entries()
                self.list_products()
                self.update_dashboard()
            else:
                QMessageBox.critical(
                    self, "Not Found", f"Product '{item_id}' does not exist."
                )

    def update_product(self):
        try:
            item_id = self.entry_id.text().strip()
            new_price = (
                float(self.entry_price.text())
                if self.entry_price.text().strip()
                else None
            )
            new_qty = (
                int(self.entry_qty.text()) if self.entry_qty.text().strip() else None
            )
            if self.inventory.update_product(item_id, new_price, new_qty):
                self._status(f"✏️ '{item_id}' updated.")
                self.list_products()
                self.update_dashboard()
            else:
                QMessageBox.critical(
                    self, "Not Found", f"Product '{item_id}' does not exist."
                )
        except ValueError:
            QMessageBox.critical(self, "Input Error", "Invalid numeric value.")

    def list_products(self):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        for p in self.inventory.products.values():
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(p.item_id))
            self.table.setItem(row, 1, QTableWidgetItem(p.name))
            price_item = QTableWidgetItem()
            price_item.setData(Qt.DisplayRole, p.price)
            self.table.setItem(row, 2, price_item)
            qty_item = QTableWidgetItem()
            qty_item.setData(Qt.DisplayRole, p.get_quantity())
            self.table.setItem(row, 3, qty_item)
            self.table.setItem(row, 4, QTableWidgetItem(p.category))
        self.table.setSortingEnabled(True)

    def update_dashboard(self):
        # 刷新圖表
        if self.chart_canvas:
            self.chart_canvas.setParent(None)
            plt.close("all")
            self.chart_canvas = None

        summary = self.inventory.category_summary()
        if summary:
            fig, ax = plt.subplots(figsize=(5, 3.5), facecolor="#1c1c1c")
            ax.set_facecolor("#1c1c1c")
            ax.pie(
                summary.values(),
                labels=summary.keys(),
                autopct="%1.1f%%",
                startangle=90,
                textprops={"color": "#dddddd", "fontsize": 10},
            )
            ax.set_title("Inventory by Category", color="#64b5f6", fontsize=13, pad=10)
            fig.tight_layout()
            self.chart_canvas = FigureCanvas(fig)
            self.chart_canvas.setSizePolicy(
                QSizePolicy.Expanding, QSizePolicy.Expanding
            )
            self.chart_frame.layout().addWidget(self.chart_canvas)

        # 刷新 KPI
        self.kpi_total_qty.update_value(str(self.inventory.total_quantity()))
        self.kpi_low_stock.update_value(str(self.inventory.low_stock_count()))
        self.kpi_avg_price.update_value(f"${self.inventory.avg_price():.2f}")
        self.kpi_cat_count.update_value(str(self.inventory.category_count()))
