import uuid

from typing import List

from fastapi import HTTPException

from lavoro_company_api.database.queries import (
    fetch_employee_ids,
    insert_and_select_job_post,
    insert_assignees,
)
from lavoro_library.models import CreateJobPostRequest


def create_job_post_and_add_assignees(company_id: uuid.UUID, payload: CreateJobPostRequest):
    validate_assignees(company_id, payload.assignees)
    job_post = payload.model_dump(exclude={"assignees"})
    assignees = payload.assignees
    created_job_post = insert_and_select_job_post(company_id, **job_post)
    if not created_job_post:
        raise HTTPException(status_code=400, detail="Job post could not be created")
    for assignee in assignees:
        insert_assignees(created_job_post.id, assignee)
    return {"detail": "Job post created"}


def validate_assignees(company_id: uuid.UUID, assignees: List[uuid.UUID]):
    employee_ids = fetch_employee_ids(company_id)
    for assignee in assignees:
        if assignee not in employee_ids:
            raise HTTPException(status_code=400, detail="Assignee is not an employee of the company")

