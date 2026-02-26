import sys
import requests
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QCheckBox,
    QSystemTrayIcon,
    QMenu,
    QStyle
)
from PyQt6.QtGui import QAction, QCursor
from PyQt6.QtCore import Qt, QEvent

ESP_IP = "192.168.1.126"  # your ESP32 IP


def send(cmd):
    try:
        requests.get(f"http://{ESP_IP}/{cmd}", timeout=2)
        print(f"Sent: {cmd}")
    except:
        print("ESP32 not reachable")


class ToggleRow(QWidget):
    def __init__(self, label, on_cmd, off_cmd):
        super().__init__()

        self.on_cmd = on_cmd
        self.off_cmd = off_cmd

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label)
        self.toggle = QCheckBox()

        # Use toggled (boolean) instead of stateChanged
        self.toggle.toggled.connect(self.handle_toggle)

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.toggle)

        self.setLayout(layout)

    def handle_toggle(self, checked):
        if checked:
            send(self.on_cmd)
        else:
            send(self.off_cmd)


class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )

        self.setFixedSize(260, 160)

        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Room Control")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        light = ToggleRow("Light", "lighton", "lightoff")
        fan = ToggleRow("Fan", "fanon", "fanoff")

        layout.addWidget(title)
        layout.addWidget(light)
        layout.addWidget(fan)

        self.setLayout(layout)

        # Modern dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
                border-radius: 14px;
            }
            QLabel {
                font-size: 14px;
            }
            QCheckBox::indicator {
                width: 40px;
                height: 20px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #555;
                border-radius: 10px;
            }
            QCheckBox::indicator:checked {
                background-color: #00c853;
                border-radius: 10px;
            }
        """)

    # Auto-hide when losing focus
    def focusOutEvent(self, event):
        self.hide()
        super().focusOutEvent(event)


app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

if not QSystemTrayIcon.isSystemTrayAvailable():
    print("System tray not available")
    sys.exit(1)

panel = ControlPanel()

# Use built-in safe icon
icon = app.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)

tray = QSystemTrayIcon(icon, app)
tray.setToolTip("Room Control")

# Right-click menu
menu = QMenu()
exit_action = QAction("Exit")
exit_action.triggered.connect(app.quit)
menu.addAction(exit_action)
tray.setContextMenu(menu)


def toggle_panel(reason):
    if reason == QSystemTrayIcon.ActivationReason.Trigger:
        if panel.isVisible():
            panel.hide()
        else:
            pos = QCursor.pos()

            x = pos.x() - panel.width() // 2
            y = pos.y() - panel.height()

            panel.move(x, y)
            panel.show()
            panel.activateWindow()


tray.activated.connect(toggle_panel)
tray.show()

print("Tray app running...")

sys.exit(app.exec())