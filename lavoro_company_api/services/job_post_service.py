from typing import List
import uuid

from fastapi import HTTPException

from lavoro_company_api.database import queries
from lavoro_library.model.company_api.dtos import CreateAssigneesDTO, CreateJobPostDTO, UpdateJobPostDTO


def create_job_post(company_id: uuid.UUID, payload: CreateJobPostDTO):
    job_post = payload.model_dump(exclude={"assignees"})
    created_job_post = queries.create_and_get_job_post(company_id, **job_post)
    if not created_job_post:
        raise HTTPException(status_code=400, detail="Job post could not be created")
    return created_job_post


def create_assignees(job_post_id: uuid.UUID, assignees: CreateAssigneesDTO):
    employee_ids = queries.get_employee_ids_by_job_post_id(job_post_id)
    previous_assignees = queries.get_assignees(job_post_id)
    for assignee in assignees:
        if assignee not in employee_ids:
            raise HTTPException(status_code=400, detail="Assignee is not an employee of the company")
        if assignee in previous_assignees:
            raise HTTPException(status_code=400, detail="Assignee is already assigned to this job post")
    return queries.create_assignees(job_post_id, assignees)


def update_job_post(job_post_id: uuid.UUID, payload: UpdateJobPostDTO):
    result = queries.update_job_post(job_post_id, payload)
    if not result:
        raise HTTPException(status_code=400, detail="Job post could not be updated")
    return result


def update_job_post(job_post_id: uuid.UUID, payload: UpdateJobPostDTO):
    result = queries.update_job_post(job_post_id, payload)
    if not result:
        raise HTTPException(status_code=400, detail="Job post could not be updated")
    return result


def get_job_post(job_post_id: uuid.UUID):
    job_post = queries.get_job_post_by_id(job_post_id)
    if not job_post:
        raise HTTPException(status_code=404, detail="Job post not found")
    return job_post


def get_job_posts_by_company(company_id: uuid.UUID):
    job_posts = queries.get_job_posts_by_company(company_id)
    return job_posts


def get_job_posts_by_recruiter(recruiter_id: uuid.UUID):
    job_posts = queries.get_job_posts_by_recruiter(recruiter_id)
    return job_posts


def get_assignees(job_post_id: uuid.UUID):
    return queries.get_assignees(job_post_id)
