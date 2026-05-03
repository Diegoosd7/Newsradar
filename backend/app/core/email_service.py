import logging
import os
import smtplib
from email.message import EmailMessage
from typing import Optional


logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self) -> None:
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", "0") or "0")
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.smtp_from = os.getenv("SMTP_FROM")
        self.app_base_url = os.getenv("APP_BASE_URL", "http://localhost:8000")
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

    def send_verification_email(self, recipient_email: str, token: str) -> None:
        verification_url = (
            f"{self.app_base_url.rstrip('/')}/api/v1/auth/verify-email?token={token}"
        )
        message = EmailMessage()
        message["Subject"] = "Verifica tu cuenta de NewsRadar"
        message["From"] = self._require_setting(self.smtp_from, "SMTP_FROM")
        message["To"] = recipient_email
        message.set_content(
            "Tu cuenta de NewsRadar ya está creada.\n\n"
            "Para verificar tu email, abre este enlace:\n"
            f"{verification_url}\n\n"
            "Este enlace caduca en 24 horas."
        )
        self._send_message(message)

    def send_password_reset_email(self, recipient_email: str, token: str) -> None:
        reset_url = f"{self.frontend_url.rstrip('/')}/reset-password?token={token}"
        message = EmailMessage()
        message["Subject"] = "Recuperación de contraseña de NewsRadar"
        message["From"] = self._require_setting(self.smtp_from, "SMTP_FROM")
        message["To"] = recipient_email
        message.set_content(
            "Has solicitado restablecer tu contraseña en NewsRadar.\n\n"
            "Para elegir una nueva contraseña, haz clic en el siguiente enlace:\n"
            f"{reset_url}\n\n"
            "Este enlace caducará en 1 hora. Si no has solicitado esto, ignora este correo."
        )
        self._send_message(message)

    def send_alert_notification_email(
        self,
        recipient_email: str,
        alert_name: str,
        source_name: str,
        news_datetime_text: str,
        title: str,
        summary: Optional[str],
    ) -> None:
        message = EmailMessage()
        message["Subject"] = f"Actualización de {alert_name} en {news_datetime_text}"
        message["From"] = self._require_setting(self.smtp_from, "SMTP_FROM")
        message["To"] = recipient_email
        message.set_content(
            "Se ha detectado una noticia que coincide con tu alerta.\n\n"
            f"Origen: {source_name}\n"
            f"Fecha/hora: {news_datetime_text}\n"
            f"Título: {title}\n"
            f"Resumen: {summary or 'Sin resumen disponible.'}\n"
        )
        self._send_message(message)

    def _send_message(self, message: EmailMessage) -> None:
        smtp_host = self._require_setting(self.smtp_host, "SMTP_HOST")
        if not self.smtp_port:
            raise RuntimeError("Falta la variable de entorno SMTP_PORT")

        if self.smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, self.smtp_port) as smtp:
                self._login_if_needed(smtp)
                smtp.send_message(message)
            return

        with smtplib.SMTP(smtp_host, self.smtp_port) as smtp:
            smtp.ehlo()
            if self.smtp_port in {587, 2525}:
                smtp.starttls()
                smtp.ehlo()
            self._login_if_needed(smtp)
            smtp.send_message(message)

    def _login_if_needed(self, smtp: smtplib.SMTP) -> None:
        if self.smtp_user and self.smtp_password:
            smtp.login(self.smtp_user, self.smtp_password)

    def _require_setting(self, value: Optional[str], name: str) -> str:
        if not value:
            raise RuntimeError(f"Falta la variable de entorno {name}")
        return value