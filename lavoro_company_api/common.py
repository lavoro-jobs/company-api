import os
from pydantic import EmailStr

from lavoro_library.email import send_email


FRONTEND_URL = os.environ["FRONTEND_URL"]


def send_invite_email(email: EmailStr, token: str, company_name: str):
    message_html = f"""
    <html>
        <body>
            <h1>You have been invited to join {company_name}</h1>
            <p>Join the company by clicking on the link: <a href="{FRONTEND_URL}/join-company/{token}">{FRONTEND_URL}/join-company/{token}</a></p>
        </body>
    </html>
    """

    return send_email(email, f"Lavoro - Invitation to join {company_name}", message_html)
