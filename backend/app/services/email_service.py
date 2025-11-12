from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from app.core.config import settings

def send_notification_email(email_to: str, linha: str, tempo_estimado_min: int):
    minutos_arredondados = int(tempo_estimado_min)
    message = Mail(
        from_email=settings.EMAIL_FROM,
        to_emails=email_to,
        subject=f"Alerta Maravi Bus: Seu ônibus da linha {linha} está chegando!",
        html_content=f"""
        <div style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2>Olá!</h2>
            <p>Seu alerta para a linha <strong>{linha}</strong> foi ativado.</p>
            <p>Um ônibus está a aproximadamente <strong>{minutos_arredondados} minutos</strong> do seu ponto de partida cadastrado.</p>
            <br>
            <p>Tenha uma boa viagem!</p>
            <br>
            <p><em>Equipe Maravi Bus Alertas</em></p>
        </div>
        """
    )
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"E-mail enviado. Status Code: {response.status_code}")
    except Exception as e:
        # Mostra o erro no log
        print(f"SERVIÇO: Erro ao enviar e-mail via SendGrid: {e}")
        if hasattr(e, 'body'):
            print(f"Detalhe do erro: {e.body}")