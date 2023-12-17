import base64
import uuid
from datetime import datetime

from typing import List

from pydantic import EmailStr
from typing import Union

from lavoro_company_api.database import db

from lavoro_library.model.company_api.db_models import (
    Assignee,
    Company,
    JobPost,
    RecruiterProfile,
    InviteToken,
    RecruiterRole,
)
from lavoro_library.model.company_api.dtos import (
    RecruiterProfileWithCompanyNameDTO,
    UpdateJobPostDTO,
    UpdateRecruiterProfileDTO,
)
from lavoro_library.model.shared import Point


def get_company_by_id(company_id: uuid.UUID):
    query_tuple = ("SELECT * FROM companies WHERE id = %s", (company_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return Company(**result["result"][0])
    else:
        return None


def get_company_by_recruiter(account_id: uuid.UUID):
    query_tuple = (
        """
        SELECT * FROM companies
        WHERE id = (
            SELECT company_id FROM recruiter_profiles
            WHERE account_id = %s
        );
        """,
        (account_id,),
    )
    result = db.execute_one(query_tuple)
    if result["result"]:
        return Company(**result["result"][0])
    else:
        return None


def create_and_get_company(name: str, description: str, logo: Union[bytes, None]):
    columns = ["name", "description"]
    values = [name, description]

    if logo:
        columns.append("logo")
        values.append(base64.b64decode(logo))

    query = f"""
        INSERT INTO companies ({", ".join(columns)})
        VALUES ({", ".join(["%s"] * len(columns))})
        RETURNING *;
        """

    result = db.execute_one((query, tuple(values)))
    if result["result"]:
        return Company(**result["result"][0])
    else:
        return None


def get_recruiter_profile(account_id: uuid.UUID):
    query_tuple = ("SELECT * FROM recruiter_profiles WHERE account_id = %s", (account_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return RecruiterProfile(**result["result"][0])
    else:
        return None


def update_recruiter_profile(id: uuid.UUID, form_data: UpdateRecruiterProfileDTO):
    update_fields = []
    query_params = []

    for field, value in form_data.model_dump(exclude_unset=True).items():
        if value is None:
            continue
        if value == "":
            value = None
        update_fields.append(f"{field} = %s")
        query_params.append(value)

    query_params.append(id)

    query = f"UPDATE recruiter_profiles SET {', '.join(update_fields)} WHERE account_id = %s"
    result = db.execute_one((query, tuple(query_params)))

    if result["affected_rows"]:
        return result["affected_rows"] == 1
    return None


def update_recruiter_profile(id: uuid.UUID, form_data: UpdateRecruiterProfileDTO):
    update_fields = []
    query_params = []

    for field, value in form_data.model_dump(exclude_unset=True).items():
        if value is None:
            continue
        if value == "":
            value = None
        update_fields.append(f"{field} = %s")
        query_params.append(value)

    query_params.append(id)

    query = f"UPDATE recruiter_profiles SET {', '.join(update_fields)} WHERE account_id = %s"
    result = db.execute_one((query, tuple(query_params)))

    if result["affected_rows"]:
        return result["affected_rows"] == 1
    return None


def update_recruiter_profile(id: uuid.UUID, form_data: UpdateRecruiterProfileDTO):
    update_fields = []
    query_params = []

    for field, value in form_data.model_dump(exclude_unset=True).items():
        if value is None:
            continue
        if value == "":
            value = None
        update_fields.append(f"{field} = %s")
        query_params.append(value)

    query_params.append(id)

    query = f"UPDATE recruiter_profiles SET {', '.join(update_fields)} WHERE account_id = %s"
    result = db.execute_one((query, tuple(query_params)))

    if result["affected_rows"]:
        return result["affected_rows"] == 1
    return None


def get_recruiter_profile_with_company_name(account_id: uuid.UUID):
    query_tuple = (
        """
        SELECT recruiter_profiles.*, companies.name AS company_name
        FROM recruiter_profiles
        LEFT JOIN companies
        ON recruiter_profiles.company_id = companies.id
        WHERE recruiter_profiles.account_id = %s;
        """,
        (account_id,),
    )
    result = db.execute_one(query_tuple)
    if result["result"]:
        return RecruiterProfileWithCompanyNameDTO(**result["result"][0])
    else:
        return None


def create_recruiter_profile(
    first_name: str,
    last_name: str,
    account_id: uuid.UUID,
    recruiter_role: RecruiterRole,
    company_id: uuid.UUID = None,
):
    query_tuple = (
        """
        INSERT INTO recruiter_profiles (first_name, last_name, company_id, account_id, recruiter_role)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (first_name, last_name, company_id, account_id, recruiter_role),
    )
    result = db.execute_one(query_tuple)
    return result["affected_rows"] == 1


def update_recruiter_company(account_id: uuid.UUID, company_id: uuid.UUID):
    query_tuple = (
        """
        UPDATE recruiter_profiles
        SET company_id = %s
        WHERE account_id = %s;
        """,
        (company_id, account_id),
    )
    result = db.execute_one(query_tuple)
    return result["affected_rows"] == 1


def create_invite_token_and_revoke_old(company_id: uuid.UUID, new_recruiter_email: EmailStr, token: str):
    query_tuple_list = [
        (
            """
            DELETE FROM invite_tokens
            WHERE email = %s AND company_id = %s;
            """,
            (new_recruiter_email, company_id),
        ),
        (
            """
            INSERT INTO invite_tokens (email, company_id, token)
            VALUES (%s, %s, %s);
            """,
            (new_recruiter_email, company_id, token),
        ),
    ]
    result = db.execute_many(query_tuple_list)
    return result["affected_rows"] > 0


def get_invitation(token: str):
    query_tuple = ("SELECT * FROM invite_tokens WHERE token = %s", (token,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return InviteToken(**result["result"][0])
    else:
        return None


def delete_invitation(token: str):
    query_tuple = ("DELETE FROM invite_tokens WHERE token = %s", (token,))
    result = db.execute_one(query_tuple)
    return result["affected_rows"] == 1


def create_and_get_job_post(
    company_id: uuid.UUID,
    position_id: int,
    description: str,
    education_level_id: int,
    skill_ids: list,
    work_type_id: int,
    seniority_level: int,
    work_location: Point,
    contract_type_id: int,
    salary_min: float,
    salary_max: float,
    end_date: datetime,
):
    query = """
        INSERT INTO job_posts (
            company_id,
            position_id,
            description,
            education_level_id,
            skill_ids,
            work_type_id,
            seniority_level,
            work_location,
            contract_type_id,
            salary_min,
            salary_max,
            end_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
    """
    point = (work_location.get("longitude"), work_location.get("latitude"))

    query_tuple = (
        query,
        (
            company_id,
            position_id,
            description,
            education_level_id,
            skill_ids,
            work_type_id,
            seniority_level,
            point,
            contract_type_id,
            salary_min,
            salary_max,
            end_date,
        ),
    )

    result = db.execute_one(query_tuple)
    if result["result"]:
        return JobPost(**result["result"][0])
    else:
        return None


def update_job_post(
    job_post_id: uuid.UUID,
    form_data: UpdateJobPostDTO,
):
    prepare_tuple = prepare_fields(job_post_id, form_data)
    update_fields = prepare_tuple[0]
    query_params = prepare_tuple[1]

    query = f"UPDATE job_posts SET {', '.join(update_fields)} WHERE id = %s"
    result = db.execute_one((query, tuple(query_params)))

    if result["affected_rows"]:
        return result["affected_rows"] == 1
    return None


def prepare_fields(id: uuid.UUID, form_data: UpdateJobPostDTO):  # tu nadodat union sa UpdateAsssigneesDTO
    update_fields = []
    query_params = []

    for field, value in form_data.model_dump(exclude_unset=True).items():
        if value is None:
            continue
        if value == "":
            value = None
        if field == "work_location":
            update_fields.append(f"{field} = point(%s, %s)")
            longitude = value.get("longitude")
            latitude = value.get("latitude")
            query_params.extend([longitude, latitude])
        else:
            update_fields.append(f"{field} = %s")
            query_params.append(value)

    query_params.append(id)
    return update_fields, query_params


def create_assignees(job_post_id: uuid.UUID, assignees: List[uuid.UUID]):
    query = """
        INSERT INTO assignees (job_post_id, recruiter_account_id)
        VALUES (%s, %s)
        RETURNING *;
        """
    query_tuple_list = [(query, (job_post_id, assignee)) for assignee in assignees]
    result = db.execute_many(query_tuple_list)
    if result["result"]:
        return [Assignee(**row) for row in result["result"]]
    else:
        return []


def get_employee_ids_by_job_post_id(job_post_id: uuid.UUID):
    query_tuple = (
        """
        SELECT recruiter_profiles.account_id
        FROM recruiter_profiles
        LEFT JOIN companies
        ON recruiter_profiles.company_id = companies.id
        LEFT JOIN job_posts
        ON companies.id = job_posts.company_id
        WHERE job_posts.id = %s;
        """,
        (job_post_id,),
    )

    result = db.execute_one(query_tuple)
    if result["result"]:
        return [row["account_id"] for row in result["result"]]
    else:
        return []


def get_company_by_id(company_id: uuid.UUID):
    query_tuple = ("SELECT * FROM companies WHERE id = %s", (company_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return Company(**result["result"][0])
    else:
        return None


def get_job_post_by_id(job_post_id: uuid.UUID):
    query_tuple = ("SELECT * FROM job_posts WHERE id = %s", (job_post_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return JobPost(**result["result"][0])
    else:
        return None


def get_job_posts_by_company(company_id: uuid.UUID):
    query_tuple = ("SELECT * FROM job_posts WHERE company_id = %s", (company_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return [JobPost(**row) for row in result["result"]]
    else:
        return []


def get_job_posts_by_recruiter(recruiter_id: uuid.UUID):
    query_tuple = (
        """
        SELECT job_posts.*
        FROM job_posts
        LEFT JOIN assignees
        ON job_posts.id = assignees.job_post_id
        WHERE assignees.recruiter_account_id = %s;
        """,
        (recruiter_id,),
    )
    result = db.execute_one(query_tuple)
    if result["result"]:
        return [JobPost(**row) for row in result["result"]]
    else:
        return []


def get_assignees(job_post_id: uuid.UUID):
    query_tuple = (
        """
        SELECT recruiter_profiles.*
        FROM assignees
        LEFT JOIN recruiter_profiles
        ON assignees.recruiter_account_id = recruiter_profiles.account_id
        WHERE job_post_id = %s;
        """,
        (job_post_id,),
    )
    result = db.execute_one(query_tuple)
    if result["result"]:
        return [RecruiterProfile(**row) for row in result["result"]]
    else:
        return []


def get_recruiters_by_company(company_id: uuid.UUID):
    query_tuple = (
        """
        SELECT *
        FROM recruiter_profiles
        WHERE company_id = %s;
        """,
        (company_id,),
    )
    result = db.execute_one(query_tuple)
    if result["result"]:
        return [RecruiterProfile(**row) for row in result["result"]]
    else:
        return []
