from typing import List
import uuid

from fastapi import APIRouter

from lavoro_company_api.services import job_post_service
from lavoro_library.model.company_api.dtos import CreateAssigneesDTO, CreateJobPostDTO

router = APIRouter(prefix="/job-post", tags=["job-post"])


@router.post("/create-job-post/{company_id}")
def create_job_post(company_id: uuid.UUID, payload: CreateJobPostDTO):
    return job_post_service.create_job_post(company_id, payload)


@router.post("/create-assignees/{job_post_id}")
def create_assignees(job_post_id: uuid.UUID, payload: CreateAssigneesDTO):
    return job_post_service.create_assignees(job_post_id, payload)


@router.get("/get-job-post")
def get_job_post(job_post_id: uuid.UUID):
    return job_post_service.get_job_post(job_post_id)


@router.get("/get-job-posts-by-company/{company_id}")
def get_job_posts_by_company(company_id: uuid.UUID):
    return job_post_service.get_job_posts_by_company(company_id)


@router.get("/get-job-posts-by-recruiter/{recruiter_id}")
def get_job_posts_by_recruiter(recruiter_id: uuid.UUID):
    return job_post_service.get_job_posts_by_recruiter(recruiter_id)
