import uuid

from fastapi import HTTPException

from lavoro_company_api.database.queries import update_recruiter_company


def add_recruiter_to_company(company_id: uuid.UUID, account_id: uuid.UUID):
    result = update_recruiter_company(account_id, company_id)
    if not result:
        raise HTTPException(status_code=400, detail="Recruiter company could not be updated")
    return {"detail": "Recruiter added to company"}
