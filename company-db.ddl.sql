CREATE EXTENSION "uuid-ossp";

CREATE TYPE recruiter_role AS ENUM ('admin', 'employee');

CREATE TABLE IF NOT EXISTS recruiter_profiles (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    company_id uuid NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    account_id uuid NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    recruiter_role recruiter_role NOT NULL
);

CREATE TABLE IF NOT EXISTS companies (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    logo_url VARCHAR(255),
    description TEXT
);

CREATE TABLE IF NOT EXISTS job_posts (
    id uuid DEFAULT uuid_generate_v4() PRIMARY KEY,
    position_id uuid NOT NULL REFERENCES position_catalog(id) ON DELETE RESTRICT,
    description TEXT,
    education_level_id uuid NOT NULL REFERENCES education_catalog(id) ON DELETE RESTRICT,
    skills_id uuid NOT NULL REFERENCES skills_catalog(id) ON DELETE RESTRICT,
    work_type_id uuid NOT NULL REFERENCES work_type_catalog(id) ON DELETE RESTRICT,
    work_location POINT,
    contract_type_id uuid NOT NULL REFERENCES contract_type_catalog(id) ON DELETE RESTRICT,
    salary_min INT,
    salary_max INT,
    created_on_date TIMESTAMP NOT NULL,
    last_updated_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assignees (
    recruiter_id uuid NOT NULL REFERENCES recruiter_profiles(id) ON DELETE CASCADE,
    job_post_id uuid NOT NULL REFERENCES job_posts(id) ON DELETE CASCADE,
    PRIMARY KEY (recruiter_id, job_post_id)
);
