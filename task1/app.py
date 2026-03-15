import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from login import LoginDialog
from gui import InventoryApp

USERS: dict[str, dict] = {
    "admin": {"password": "1234", "role": "admin"},
    "user": {"password": "5678", "role": "viewer"},
}
MAX_ATTEMPTS = 3


class AppController:
    def __init__(self):
        self.main_window: InventoryApp | None = None
        self.login_dialog: LoginDialog | None = None
        self._show_login()

    def _show_login(self):
        self.login_dialog = LoginDialog(users=USERS, max_attempts=MAX_ATTEMPTS)
        self.login_dialog.login_success.connect(self._on_login_success)
        self.login_dialog.login_cancelled.connect(QApplication.quit)
        self.login_dialog.show()

    def _on_login_success(self, username: str, role: str):
        self.login_dialog = None  # ✅ dialog 已自行 close()，只需釋放參考

        self.main_window = InventoryApp(username=username, role=role)
        self.main_window.logout_requested.connect(self._on_logout)
        self.main_window.show()

    def _on_logout(self):
        if self.main_window:
            self.main_window.close()
            self.main_window = None
        QTimer.singleShot(150, self._show_login)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setQuitOnLastWindowClosed(False)  # ✅ 視窗切換時唔會自動退出
    controller = AppController()
    sys.exit(app.exec())
