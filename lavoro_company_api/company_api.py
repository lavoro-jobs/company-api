from fastapi import APIRouter, FastAPI

from lavoro_company_api.routers.company import router as company_router
from lavoro_company_api.routers.job_post import router as job_post_router
from lavoro_company_api.routers.recruiter import router as recruiter_router

app = FastAPI()

router = APIRouter()
router.include_router(company_router)
router.include_router(job_post_router)
router.include_router(recruiter_router)

app.include_router(router)
