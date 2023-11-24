import uuid

from fastapi import APIRouter

from lavoro_company_api.helpers.company_helpers import create_company_and_update_recruiter, validate_company_creation
from lavoro_library.models import CreateCompanyRequest

router = APIRouter(prefix="/company", tags=["company"])


@router.post("/create-company/{recruiter_account_id}")
def create_company(payload: CreateCompanyRequest, recruiter_account_id: uuid.UUID):
    validate_company_creation(recruiter_account_id)
    result = create_company_and_update_recruiter(payload, recruiter_account_id)
    return result
