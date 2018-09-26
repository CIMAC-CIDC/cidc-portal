import sendgrid

from constants import SENDGRID_API_KEY
from constants import SEND_FROM_EMAIL

from sendgrid.helpers.mail import *


def send_mail(subject: str, message_text: str, to_email: str) -> bool:
    """
    Sends an email via Sendgrid. Configure API_KEY via constants.

    :param subject:
    :param message_text:
    :param to_email: Single address where the email will be sent.
    :return:
    """
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    from_email = Email(SEND_FROM_EMAIL)
    to_email = Email(to_email)
    subject = subject
    content = Content("text/plain", message_text)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

    return response.status_code == 202
