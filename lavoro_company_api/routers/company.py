import uuid

from fastapi import APIRouter

from pydantic import EmailStr


from lavoro_company_api.services import company_service

from lavoro_library.model.company_api.dtos import CreateCompanyDTO

router = APIRouter(prefix="/company", tags=["company"])


@router.post("/create-company/{recruiter_account_id}")
def create_company(payload: CreateCompanyDTO, recruiter_account_id: uuid.UUID):
    return company_service.create_company(recruiter_account_id, payload)


@router.post("/invite-recruiter/{company_id}/{new_recruiter_email}")
async def invite_recruiter(company_id: uuid.UUID, new_recruiter_email: EmailStr):
    return await company_service.invite_recruiter(company_id, new_recruiter_email)


@router.delete("/delete-invite-token/{invite_token}")
def delete_invite_token(invite_token: str):
    return company_service.delete_invitation(invite_token)
