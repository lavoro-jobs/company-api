import uuid

from fastapi import HTTPException

from lavoro_company_api.database import queries
from lavoro_library.model.company_api.dtos import CreateRecruiterProfileDTO, UpdateRecruiterProfileDTO
from lavoro_library.model.company_api.db_models import RecruiterRole


def create_recruiter_profile(account_id: uuid.UUID, recruiter_role: RecruiterRole, payload: CreateRecruiterProfileDTO):
    recruiter_profile = queries.get_recruiter_profile(account_id)
    if recruiter_profile:
        raise HTTPException(status_code=400, detail="Recruiter profile already exists")
    result = queries.create_recruiter_profile(
        payload.first_name, payload.last_name, account_id, recruiter_role, payload.company_id
    )
    if not result:
        raise HTTPException(status_code=400, detail="Recruiter profile could not be created")
    return {"detail": "Recruiter profile created"}


def get_recruiter_profile(account_id: uuid.UUID):
    recruiter_profile = queries.get_recruiter_profile(account_id)
    if not recruiter_profile:
        raise HTTPException(status_code=404, detail="Recruiter profile not found")
    return recruiter_profile


def update_recruiter_profile(account_id: uuid.UUID, form_data: UpdateRecruiterProfileDTO):
    result = queries.update_recruiter_profile(account_id, form_data)
    if not result:
        raise HTTPException(status_code=400, detail="Applicant profile could not be updated")
    return result


def get_recruiter_profile_with_company_name(account_id: uuid.UUID):
    recruiter_profile = queries.get_recruiter_profile_with_company_name(account_id)
    if not recruiter_profile:
        raise HTTPException(status_code=404, detail="Recruiter profile not found")
    return recruiter_profile


def get_invitation(invite_token: str):
    invitation = queries.get_invitation(invite_token)
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found")
    return invitation


def get_recruiters_by_company(company_id: uuid.UUID):
    recruiters = queries.get_recruiters_by_company(company_id)
    if not recruiters:
        raise HTTPException(status_code=404, detail="Recruiters not found")
    return recruiters
