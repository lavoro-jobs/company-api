import uuid

from fastapi import APIRouter

from pydantic import EmailStr

# from lavoro_company_api.database.queries import delete_invitation, get_company_by_id
# from lavoro_company_api.helpers.company_helpers import create_company_and_update_recruiter, validate_company_creation
# from lavoro_company_api.helpers.email_helpers import send_invite_email
# from lavoro_company_api.helpers.invitation_helpers import create_invite_token

from lavoro_company_api.services import company_service

# from lavoro_library.models import CreateCompanyRequest
from lavoro_library.model.company_api.dtos import CreateCompanyDTO

router = APIRouter(prefix="/company", tags=["company"])


@router.post("/create-company/{recruiter_account_id}")
def create_company(payload: CreateCompanyDTO, recruiter_account_id: uuid.UUID):
    return company_service.create_company(recruiter_account_id, payload)
    # validate_company_creation(recruiter_account_id)
    # return create_company_and_update_recruiter(payload, recruiter_account_id)


@router.post("/invite-recruiter/{company_id}/{new_recruiter_email}")
async def invite_recruiter(company_id: uuid.UUID, new_recruiter_email: EmailStr):
    return await company_service.invite_recruiter(company_id, new_recruiter_email)
    # invite_token = create_invite_token(company_id, new_recruiter_email)
    # company = get_company_by_id(company_id)
    # await send_invite_email(new_recruiter_email, invite_token, company.name)
    # return {"detail": "Recruiter invited"}


@router.delete("/delete-invite-token/{invite_token}")
def delete_invite_token(invite_token: str):
    return company_service.delete_invitation(invite_token)
    # return delete_invitation(invite_token)
