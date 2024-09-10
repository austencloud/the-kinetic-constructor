import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
    QMessageBox,
)

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SequenceSharerDialog(QDialog):
    def __init__(self, main_widget: "MainWidget", image_path):
        super().__init__(main_widget)
        self.image_path = image_path
        self.settings_manager = main_widget.settings_manager
        self.setWindowTitle("Share Sequence Image")
        self.setFixedSize(400, 200)

        # Create UI components
        layout = QVBoxLayout(self)

        self.email_label = QLabel("Recipient's Email:", self)

        # ComboBox to show saved emails
        self.email_combo_box = QComboBox(self)
        saved_emails = self.settings_manager.sequence_sharing.get_saved_emails()
        self.email_combo_box.addItems(saved_emails)
        self.email_combo_box.setEditable(True)  # Allow user to type a new email

        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_email)

        layout.addWidget(self.email_label)
        layout.addWidget(self.email_combo_box)
        layout.addWidget(self.send_button)

        self.setLayout(layout)

    def send_email(self):
        recipient_email = self.email_combo_box.currentText()
        if not recipient_email:
            QMessageBox.warning(
                self, "Input Error", "Please enter a valid email address."
            )
            return

        # Save email to settings
        self.settings_manager.sequence_sharing.add_email(recipient_email)

        from_email = os.getenv("GMAIL_USER")
        password = os.getenv("GMAIL_PASS")

        if not from_email or not password:
            QMessageBox.critical(
                self,
                "Email Setup Error",
                "Please set up your Gmail credentials using environment variables.",
            )
            return

        subject = "Your Preview Image"
        body = "Attached is the preview image."

        msg = MIMEMultipart()
        msg["From"] = from_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Attach the image file
        try:
            print(f"Attaching file from path: {self.image_path}")  # Log file path

            if not os.path.exists(self.image_path):
                QMessageBox.critical(self, "File Error", "File does not exist.")
                return

            file_size = os.path.getsize(self.image_path)
            print(f"File size: {file_size} bytes")  # Log file size

            if file_size == 0:
                QMessageBox.critical(self, "File Error", "File is empty.")
                return

            with open(self.image_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)

                # Log the file name for debugging
                filename = os.path.basename(self.image_path)
                print(f"Filename for attachment: {filename}")

                # Ensure the file name is correctly attached
                part.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{filename}"',
                )
                msg.attach(part)

        except Exception as e:
            QMessageBox.critical(
                self, "File Error", f"Failed to attach image: {str(e)}"
            )
            print(f"Attachment error: {str(e)}")  # Log the error
            return

        try:
            # Connect to Gmail's SMTP server
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, recipient_email, msg.as_string())
            QMessageBox.information(self, "Success", "Email sent successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Email Error", f"Failed to send email: {str(e)}")
            print(f"Email error: {str(e)}")  # Log email sending error
        finally:
            server.quit()
