import uuid
from datetime import datetime

from typing import List

from pydantic import EmailStr

from lavoro_company_api.database import db
from lavoro_library.models import (
    CompanyInDB,
    CompanyInvitation,
    Point,
    RecruiterProfileInDB,
    RecruiterProfileWithCompanyName,
    RecruiterRole,
)


def get_company_by_id(company_id: uuid.UUID):
    query_tuple = ("SELECT * FROM companies WHERE id = %s", (company_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return CompanyInDB(**result["result"][0])
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
        return CompanyInDB(**result["result"][0])
    else:
        return None


def insert_and_select_company(name: str, description: str, logo: bytes, account_id: uuid.UUID = None):
    query_tuple = (
        """
        INSERT INTO companies (name, description, logo)
        VALUES (%s, %s, %s)
        RETURNING *;
        """,
        (name, description, logo),
    )

    result = db.execute_one(query_tuple)
    if result["result"]:
        return CompanyInDB(**result["result"][0])
    else:
        return None


def fetch_recruiter_profile(account_id: uuid.UUID):
    query_tuple = ("SELECT * FROM recruiter_profiles WHERE account_id = %s", (account_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return RecruiterProfileInDB(**result["result"][0])
    else:
        return None


def fetch_recruiter_profile_with_company_name(account_id: uuid.UUID):
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
        return RecruiterProfileWithCompanyName(**result["result"][0])
    else:
        return None


def insert_recruiter_profile(
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


def insert_invitation_and_revoke_old(company_id: uuid.UUID, new_recruiter_email: EmailStr, token: str):
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


def fetch_invitation(token: str):
    query_tuple = ("SELECT * FROM invite_tokens WHERE token = %s", (token,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return CompanyInvitation(**result["result"][0])
    else:
        return None


def delete_invitation(token: str):
    query_tuple = ("DELETE FROM invite_tokens WHERE token = %s", (token,))
    result = db.execute_one(query_tuple)
    return result["affected_rows"] == 1


def insert_and_select_job_post(
    company_id: uuid.UUID,
    position_id: int,
    description: str,
    education_level_id: int,
    skill_id_list: list,
    work_type_id: int,
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
            skill_id_list,
            work_type_id,
            work_location,
            contract_type_id,
            salary_min,
            salary_max,
            end_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            skill_id_list,
            work_type_id,
            point,
            contract_type_id,
            salary_min,
            salary_max,
            end_date,
        ),
    )

    result = db.execute_one(query_tuple)
    if result["result"]:
        return result["result"][0]
    else:
        return None


def insert_assignees(job_post_id: uuid.UUID, assignees: List[uuid.UUID]):
    query = """
        INSERT INTO job_post_assignees (job_post_id, assignee)
        VALUES (%s, %s);
        """
    query_tuple_list = [(query, (job_post_id, assignee)) for assignee in assignees]
    result = db.execute_many(query_tuple_list)
    return result["affected_rows"] == 1


def fetch_employee_ids(company_id: uuid.UUID):
    query_tuple = ("SELECT account_id FROM recruiter_profiles WHERE company_id = %s", (company_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        return [row["account_id"] for row in result["result"]]
    else:
        return None
