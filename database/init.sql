CREATE TABLE IF NOT EXISTS health_units (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    unit_type VARCHAR(80) NOT NULL,
    municipality VARCHAR(120) NOT NULL,
    address VARCHAR(255),
    contact VARCHAR(80),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    patient_identifier VARCHAR(50) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    birth_date DATE,
    gender VARCHAR(20),
    identity_card VARCHAR(30),
    nif VARCHAR(30),
    contact VARCHAR(80),
    address VARCHAR(255),
    health_unit_id INTEGER REFERENCES health_units(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    username VARCHAR(80) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile VARCHAR(50) NOT NULL,
    health_unit_id INTEGER REFERENCES health_units(id),
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS consultations (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL REFERENCES patients(id),
    professional_name VARCHAR(255) NOT NULL,
    health_unit_id INTEGER NOT NULL REFERENCES health_units(id),
    consultation_datetime TIMESTAMP NOT NULL,
    diagnosis TEXT,
    observations TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS data_shares (
    id SERIAL PRIMARY KEY,
    source_unit_id INTEGER REFERENCES health_units(id),
    target_unit_id INTEGER REFERENCES health_units(id),
    patient_id INTEGER REFERENCES patients(id),
    shared_by VARCHAR(120),
    share_type VARCHAR(80),
    permission_level VARCHAR(40),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_patients_name ON patients(full_name);
CREATE INDEX IF NOT EXISTS idx_consultations_patient ON consultations(patient_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
