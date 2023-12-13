import uuid

from fastapi import HTTPException

from lavoro_company_api.database import queries
from lavoro_library.model.company_api.dtos import CreateJobPostDTO


def create_job_post(company_id: uuid.UUID, payload: CreateJobPostDTO):
    employee_ids = queries.get_employee_ids(company_id)
    for assignee in payload.assignees:
        if assignee not in employee_ids:
            raise HTTPException(status_code=400, detail="Assignee is not an employee of the company")
    job_post = payload.model_dump(exclude={"assignees"})
    assignees = payload.assignees
    created_job_post = queries.create_and_get_job_post(company_id, **job_post)
    if not created_job_post:
        raise HTTPException(status_code=400, detail="Job post could not be created")
    queries.create_assignees(created_job_post.id, assignees)
    return {"detail": "Job post created"}


def get_job_post(job_post_id: uuid.UUID):
    job_post = queries.get_job_post_by_id(job_post_id)
    if not job_post:
        raise HTTPException(status_code=404, detail="Job post not found")
    job_post.assignees = queries.get_assignees(job_post.id)
    return job_post


def get_job_posts_by_company(company_id: uuid.UUID):
    job_posts = queries.get_job_posts_by_company(company_id)
    for job_post in job_posts:
        job_post.assignees = queries.get_assignees(job_post.id)
    return job_posts


def get_job_posts_by_recruiter(recruiter_id: uuid.UUID):
    job_posts = queries.get_job_posts_by_recruiter(recruiter_id)
    for job_post in job_posts:
        job_post.assignees = queries.get_assignees(job_post.id)
    return job_posts
