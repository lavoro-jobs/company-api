import uuid

from fastapi import APIRouter

from lavoro_company_api.helpers.job_post_helpers import create_job_post_and_add_assignees
from lavoro_library.models import CreateJobPostRequest

router = APIRouter(prefix="/job-post", tags=["job-post"])


@router.post("/create-job-post")
def create_job_post(company_id: uuid.UUID, payload: CreateJobPostRequest):
    return create_job_post_and_add_assignees(company_id, payload)
