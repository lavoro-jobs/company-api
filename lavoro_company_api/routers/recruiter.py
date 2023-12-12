import uuid

from fastapi import APIRouter, HTTPException

# from lavoro_company_api.database.queries import (
#     fetch_recruiter_profile,
#     fetch_recruiter_profile_with_company_name,
#     insert_recruiter_profile,
# )

# from lavoro_company_api.helpers.invitation_helpers import check_invite_token
# from lavoro_company_api.helpers.recruiter_helpers import add_recruiter_to_company

from lavoro_company_api.services import recruiter_service

from lavoro_library.models import CreateRecruiterProfileWithCompanyRequest, RecruiterRole
from lavoro_library.model.company_api.db_models import RecruiterRole


router = APIRouter(prefix="/recruiter", tags=["recruiter"])


@router.post("/create-recruiter-profile/{account_id}/{recruiter_role}")
def create_recruiter_profile(
    account_id: uuid.UUID, recruiter_role: RecruiterRole, payload: CreateRecruiterProfileWithCompanyRequest
):
    return recruiter_service.create_recruiter_profile(account_id, recruiter_role, payload)
    # recruiter_profile = fetch_recruiter_profile(account_id)
    # if recruiter_profile:
    #     raise HTTPException(status_code=400, detail="Recruiter profile already exists")
    # result = insert_recruiter_profile(
    #     payload.first_name, payload.last_name, account_id, recruiter_role, payload.company_id
    # )
    # if not result:
    #     raise HTTPException(status_code=400, detail="Recruiter profile could not be created")
    # return {"detail": "Recruiter profile created"}


@router.get("/get-recruiter-profile/{account_id}")
def get_recruiter_profile(account_id: uuid.UUID):
    return recruiter_service.get_recruiter_profile(account_id)
    # recruiter_profile = fetch_recruiter_profile(account_id)
    # if not recruiter_profile:
    #     raise HTTPException(status_code=404, detail="Recruiter profile not found")
    # return recruiter_profile


@router.get("/get-recruiter-profile-with-company-name/{account_id}")
def get_recruiter_profile_with_company_name(account_id: uuid.UUID):
    return recruiter_service.get_recruiter_profile_with_company_name(account_id)
    # recruiter_profile = fetch_recruiter_profile_with_company_name(account_id)
    # if not recruiter_profile:
    #     raise HTTPException(status_code=404, detail="Recruiter profile not found")
    # return recruiter_profile


@router.get("/get-invitation/{invite_token}")
def get_invitation(invite_token: str):
    return recruiter_service.get_invitation(invite_token)


# @router.post("/join-company/{company_id}/{account_id}")
# def join_company(company_id: uuid.UUID, account_id: uuid.UUID):
#     add_recruiter_to_company(company_id, account_id)
