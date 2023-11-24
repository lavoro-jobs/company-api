import uuid

from fastapi import APIRouter, HTTPException

from lavoro_company_api.database.queries import (
    fetch_recruiter_profile,
    fetch_recruiter_profile_with_company_name,
    insert_recruiter_profile,
)
from lavoro_library.models import CreateRecruiterProfileRequest


router = APIRouter(prefix="/recruiter", tags=["recruiter"])


@router.post("/create-recruiter-profile/{account_id}")
def create_recruiter_profile(account_id: uuid.UUID, payload: CreateRecruiterProfileRequest):
    recruiter_profile = fetch_recruiter_profile(account_id)
    if recruiter_profile:
        raise HTTPException(status_code=400, detail="Recruiter profile already exists")
    result = insert_recruiter_profile(payload.first_name, payload.last_name, account_id, company_id=None)
    if not result:
        raise HTTPException(status_code=400, detail="Recruiter profile could not be created")
    return {"detail": "Recruiter profile created"}


@router.get("/get-recruiter-profile/{account_id}")
def get_recruiter_profile(account_id: uuid.UUID):
    recruiter_profile = fetch_recruiter_profile(account_id)
    if not recruiter_profile:
        raise HTTPException(status_code=404, detail="Recruiter profile not found")
    return recruiter_profile


@router.get("/get-recruiter-profile-with-company-name/{account_id}")
def get_recruiter_profile_with_company_name(account_id: uuid.UUID):
    recruiter_profile = fetch_recruiter_profile_with_company_name(account_id)
    if not recruiter_profile:
        raise HTTPException(status_code=404, detail="Recruiter profile not found")
    return recruiter_profile
