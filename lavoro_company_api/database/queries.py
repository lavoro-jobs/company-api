import base64
import uuid

from pydantic import EmailStr
from typing import Union

from lavoro_company_api.database import db

from lavoro_library.model.company_api.db_models import Company, RecruiterProfile, InviteToken, RecruiterRole
from lavoro_library.model.company_api.dtos import RecruiterProfileWithCompanyNameDTO


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


def get_company_by_id(company_id: uuid.UUID):
    query_tuple = ("SELECT * FROM companies WHERE id = %s", (company_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return Company(**result["result"][0])
    else:
        return None
<<<<<<< Updated upstream
=======


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
    query_tuple = ("SELECT recruiter_account_id FROM assignees WHERE job_post_id = %s", (job_post_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return [row["recruiter_account_id"] for row in result["result"]]
    else:
        return []
>>>>>>> Stashed changes
