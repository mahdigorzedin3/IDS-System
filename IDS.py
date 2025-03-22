import sys
import psutil
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import QTimer
import codecs
import os

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
os.environ["QT_LOGGING_RULES"] = "*.debug=false"
class IntrusionDetectionSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_security)
        self.timer.start(1500)

    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle("Intrusion Detection System - IDS")
        self.setGeometry(300, 300, 500, 400)
        layout = QVBoxLayout()
        self.status_label = QLabel("🔍 System is monitoring for security threats...")
        layout.addWidget(self.status_label)
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)
        self.start_btn = QPushButton("▶️ Start Monitoring")
        self.start_btn.clicked.connect(self.start_monitoring)
        layout.addWidget(self.start_btn)
        self.stop_btn = QPushButton("⏹ Stop Monitoring")
        self.stop_btn.clicked.connect(self.stop_monitoring)
        layout.addWidget(self.stop_btn)
        self.setLayout(layout)

    def log_alert(self, message):
        """Log alerts to the file and display them in the application"""
        self.log_area.append(message)

    def check_security(self):
        """Check system security and alert if any suspicious activity is detected"""
        try:
            cpu_usage = psutil.cpu_percent(interval=0.05)
            ram_usage = psutil.virtual_memory().percent

            if cpu_usage > 80:
                self.log_alert(f"⚠️ WARNING: High CPU usage detected! ({cpu_usage}%)")

            if ram_usage > 80:
                self.log_alert(f"⚠️ WARNING: High RAM usage detected! ({ram_usage}%)")

            suspicious_processes = ["keylogger", "malware", "notepad.exe"]
            try:
                for process in psutil.process_iter(['name']):
                    if process.info['name'].lower() in suspicious_processes:
                        self.log_alert(f"⚠️ WARNING: Suspicious process detected → {process.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

            suspicious_ports = [4444, 5555, 3389, 1337, 8080]
            for port in suspicious_ports:
              try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)  
                result = s.connect_ex(("127.0.0.1", port))  
                if result == 0:
                  self.log_alert(f"⚠️ WARNING: Suspicious open port detected → {port}")
                s.close()
              except Exception as e:
                self.log_alert(f"⚠️ ERROR: Port scan failed for {port} - {str(e)}")



        except Exception as e:
            self.log_alert(f"🚨 ERROR: An unexpected error occurred - {str(e)}")

    def start_monitoring(self):
        """Start security monitoring"""
        self.log_alert("✅ System monitoring started.")
        self.timer.start(1500)  

    def stop_monitoring(self):
        """Stop security monitoring"""
        self.log_alert("🛑 System monitoring stopped.")
        self.timer.stop()




if __name__ == '__main__':
    task_name = "MonitorLogin"
    xml_file_path = "task_definition.xml"
    app = QApplication(sys.argv)
    ex = IntrusionDetectionSystem()
    ex.show()
    sys.exit(app.exec_())
