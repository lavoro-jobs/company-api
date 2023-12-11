import base64
import uuid

from pydantic import EmailStr
from typing import Union

from lavoro_company_api.database import db
from lavoro_library.models import (
    CompanyInDB,
    CompanyInvitation,
    RecruiterProfileInDB,
    RecruiterProfileWithCompanyName,
    RecruiterRole,
)


def get_company_by_id(company_id: uuid.UUID):
    query_tuple = ("SELECT * FROM companies WHERE id = %s", (company_id,))
    result = db.execute_one(query_tuple)
    if result["result"]:
        company_in_db = CompanyInDB(**result["result"][0])
        company_in_db.logo = base64.b64encode(company_in_db.logo).decode("utf-8")
        return company_in_db
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
        company_in_db = CompanyInDB(**result["result"][0])
        company_in_db.logo = base64.b64encode(company_in_db.logo).decode("utf-8")
        return company_in_db
    else:
        return None


def insert_and_select_company(name: str, description: str, logo: Union[bytes, None], account_id: uuid.UUID = None):
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
        company_in_db = CompanyInDB(**result["result"][0])
        company_in_db.logo = base64.b64encode(company_in_db.logo).decode("utf-8")
        return company_in_db
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
