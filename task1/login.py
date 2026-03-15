from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import Qt, Signal, QTimer


class LoginDialog(QDialog):
    login_success = Signal(str, str)
    login_cancelled = Signal()

    def __init__(self, users: dict, max_attempts: int = 3, parent=None):
        super().__init__(parent)
        self._users = users
        self._max_attempts = max_attempts
        self._attempts = 0

        self.setWindowTitle("🔐 Login")
        self.setFixedSize(380, 300)
        self.setWindowFlags(Qt.Window | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)

        self._build_ui()
        self._apply_style()

        self.entry_user.returnPressed.connect(self.entry_pass.setFocus)
        self.entry_pass.returnPressed.connect(self._check_login)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(40, 30, 40, 30)
        root.setSpacing(14)

        title = QLabel("📦 Inventory System")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignCenter)
        root.addWidget(title)

        hint = QLabel("Sign in to continue")
        hint.setObjectName("hint")
        hint.setAlignment(Qt.AlignCenter)
        root.addWidget(hint)

        root.addSpacing(4)

        form = QFormLayout()
        form.setSpacing(10)

        self.entry_user = QLineEdit()
        self.entry_user.setPlaceholderText("Username")
        self.entry_user.setObjectName("input")

        self.entry_pass = QLineEdit()
        self.entry_pass.setPlaceholderText("Password")
        self.entry_pass.setEchoMode(QLineEdit.Password)
        self.entry_pass.setObjectName("input")

        form.addRow("Username:", self.entry_user)
        form.addRow("Password:", self.entry_pass)
        root.addLayout(form)

        self.error_label = QLabel("")
        self.error_label.setObjectName("error")
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.hide()
        root.addWidget(self.error_label)

        self.login_btn = QPushButton("🔑  Login")
        self.login_btn.setObjectName("login_btn")
        self.login_btn.clicked.connect(self._check_login)
        root.addWidget(self.login_btn)

    def _apply_style(self):
        self.setStyleSheet(
            """
            QDialog               { background: #1e1e1e; }
            QLabel                { color: #cccccc; font-size: 13px; }
            QLabel#title          { color: #64b5f6; font-size: 19px; font-weight: bold; }
            QLabel#hint           { color: #777777; font-size: 11px; }
            QLabel#error          { color: #e74c3c; font-size: 11px; }
            QLineEdit#input {
                background: #2a2a2a; color: #eeeeee;
                border: 1px solid #555; border-radius: 5px;
                padding: 6px 10px; font-size: 13px;
            }
            QLineEdit#input:focus { border: 1px solid #64b5f6; }
            QPushButton#login_btn {
                background: #27ae60; color: white;
                border-radius: 5px; padding: 9px;
                font-size: 14px; font-weight: bold;
            }
            QPushButton#login_btn:hover    { background: #2ecc71; }
            QPushButton#login_btn:pressed  { background: #1e8449; }
            QPushButton#login_btn:disabled { background: #555555; }
        """
        )

    # ✅ _check_login 係獨立方法，唔係 _apply_style 入面
    def _check_login(self):
        username = self.entry_user.text().strip()
        password = self.entry_pass.text()
        user = self._users.get(username)

        if user and user["password"] == password:
            self.login_success.emit(username, user["role"])
            QTimer.singleShot(0, self.close)
            return

        self._attempts += 1
        self.entry_pass.clear()
        remaining = self._max_attempts - self._attempts

        if remaining > 0:
            self.error_label.setText(
                f"❌ Invalid credentials — {remaining} attempt(s) left"
            )
            self.error_label.show()
        else:
            self.error_label.setText("🔒 Too many failed attempts. Closing...")
            self.error_label.show()
            self.login_btn.setDisabled(True)
            self.entry_user.setDisabled(True)
            self.entry_pass.setDisabled(True)
            QTimer.singleShot(2000, self.login_cancelled.emit)
