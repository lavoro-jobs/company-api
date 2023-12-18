import secrets
import uuid

from fastapi import HTTPException
from lavoro_company_api.common import send_invite_email

from lavoro_company_api.database import queries
from lavoro_library.model.company_api.db_models import RecruiterRole
from lavoro_library.model.company_api.dtos import CreateCompanyDTO, UpdateCompanyDTO


def create_company(recruiter_account_id: uuid.UUID, payload: CreateCompanyDTO):
    recruiter_profile = queries.get_recruiter_profile(recruiter_account_id)
    if not recruiter_profile:
        raise HTTPException(status_code=404, detail="Recruiter profile not found")
    if not recruiter_profile.recruiter_role == RecruiterRole.admin:
        raise HTTPException(status_code=403, detail="Only admin recruiters can create companies")
    if recruiter_profile.company_id:
        raise HTTPException(status_code=400, detail="Recruiter already has a company")
    created_company = queries.create_and_get_company(payload.name, payload.description, payload.logo)
    if not created_company:
        raise HTTPException(status_code=400, detail="Company could not be created")
    result = queries.update_recruiter_company(recruiter_account_id, created_company.id)
    if not result:
        raise HTTPException(status_code=400, detail="Recruiter company could not be updated")
    return result


def get_company(company_id: uuid.UUID):
    company = queries.get_company_by_id(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


def update_company(company_id: uuid.UUID, payload: UpdateCompanyDTO):
    result = queries.update_company(company_id, payload)
    if not result:
        raise HTTPException(status_code=400, detail="Company could not be updated")
    return result


async def invite_recruiter(company_id: uuid.UUID, new_recruiter_email: str):
    invite_token = secrets.token_urlsafe(32)
    result = queries.create_invite_token_and_revoke_old(company_id, new_recruiter_email, invite_token)
    if not result:
        raise HTTPException(status_code=400, detail="Invitation could not be created")
    company = queries.get_company_by_id(company_id)
    await send_invite_email(new_recruiter_email, invite_token, company.name)


def delete_invitation(invite_token: str):
    result = queries.delete_invitation(invite_token)
    if not result:
        raise HTTPException(status_code=400, detail="Invitation could not be deleted")
    return result
