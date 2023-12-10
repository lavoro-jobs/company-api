import uuid

from fastapi import HTTPException

from lavoro_company_api.database.queries import (
    fetch_recruiter_profile,
    insert_and_select_company,
    update_recruiter_company,
)

# from lavoro_library.models import CreateCompanyRequest, RecruiterRole
from lavoro_library.model.company_api.db_models import RecruiterRole
from lavoro_library.model.company_api.dtos import CreateCompanyDTO


def validate_company_creation(recruiter_account_id: uuid.UUID):
    recruiter_profile = fetch_recruiter_profile(recruiter_account_id)
    if not recruiter_profile:
        raise HTTPException(status_code=404, detail="Recruiter profile not found")
    if not recruiter_profile.recruiter_role == RecruiterRole.admin:
        raise HTTPException(status_code=403, detail="Only admin recruiters can create companies")
    if recruiter_profile.company_id:
        raise HTTPException(status_code=400, detail="Recruiter already has a company")


def create_company_and_update_recruiter(payload: CreateCompanyDTO, recruiter_account_id: uuid.UUID):
    created_company = insert_and_select_company(payload.name, payload.description, payload.logo)
    if not created_company:
        raise HTTPException(status_code=400, detail="Company could not be created")
    result = update_recruiter_company(recruiter_account_id, created_company.id)
    if not result:
        raise HTTPException(status_code=400, detail="Recruiter company could not be updated")
    return {"detail": "Company created"}
