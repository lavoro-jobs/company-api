import secrets
import uuid

from fastapi import HTTPException

from lavoro_company_api.database.queries import insert_invitation_and_revoke_old, fetch_invitation


def generate_invite_token():
    return secrets.token_urlsafe(32)


def create_invite_token(company_id: uuid.UUID, new_recruiter_email: str):
    invite_token = generate_invite_token()
    insert_invitation_and_revoke_old(company_id, new_recruiter_email, invite_token)
    return invite_token


def check_invite_token(invite_token: str):
    invitation = fetch_invitation(invite_token)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    return invitation
