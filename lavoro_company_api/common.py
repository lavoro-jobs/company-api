from pydantic import EmailStr

from lavoro_library.email import send_email


def send_invite_email(email: EmailStr, token: str, company_name: str):
    message_html = f"""
    <html>
        <body>
            <h1>You have been invited to join {company_name}</h1>
            <p>Join the company by clicking on the link: <a href="http://localhost:3000/join-company/{token}">http://localhost:3000/join-company/{token}</a></p>
        </body>
    </html>
    """

    return send_email(email, f"Lavoro - Invitation to join {company_name}", message_html)
