import uuid

from fastapi import APIRouter, status

from lavoro_company_api.services import recruiter_service

from lavoro_library.model.company_api.db_models import RecruiterRole
from lavoro_library.model.company_api.dtos import CreateRecruiterProfileDTO, UpdateRecruiterProfileDTO


router = APIRouter(prefix="/recruiter", tags=["recruiter"])


@router.post("/create-recruiter-profile/{account_id}/{recruiter_role}")
def create_recruiter_profile(account_id: uuid.UUID, recruiter_role: RecruiterRole, payload: CreateRecruiterProfileDTO):
    return recruiter_service.create_recruiter_profile(account_id, recruiter_role, payload)


@router.get("/get-recruiter-profile/{account_id}")
def get_recruiter_profile(account_id: uuid.UUID):
    return recruiter_service.get_recruiter_profile(account_id)


@router.patch("/update-recruiter-profile/{account_id}", status_code=status.HTTP_200_OK)
def update_applicant(account_id: uuid.UUID, form_data: UpdateRecruiterProfileDTO):
    return recruiter_service.update_recruiter_profile(account_id, form_data)


@router.get("/get-recruiter-profile-with-company-name/{account_id}")
def get_recruiter_profile_with_company_name(account_id: uuid.UUID):
    return recruiter_service.get_recruiter_profile_with_company_name(account_id)


@router.get("/get-invitation/{invite_token}")
def get_invitation(invite_token: str):
    return recruiter_service.get_invitation(invite_token)


@router.get("/get-recruiters-by-company/{company_id}")
def get_recruiters_by_company(company_id: uuid.UUID):
    return recruiter_service.get_recruiters_by_company(company_id)
