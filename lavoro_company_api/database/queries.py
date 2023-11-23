import uuid

from lavoro_company_api.database import db
from lavoro_library.models import CompanyInDB, RecruiterProfileInDB, RecruiterProfileWithCompanyName


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


def insert_recruiter_profile(first_name: str, last_name: str, account_id: uuid.UUID, company_id: uuid.UUID = None):
    query_tuple = (
        """
        INSERT INTO recruiter_profiles (first_name, last_name, company_id, account_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """,
        (first_name, last_name, company_id, account_id),
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
