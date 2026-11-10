from uuid import uuid4

from fastapi.testclient import TestClient

from server.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_login_success():
    response = client.post("/api/login", json={"username": "admin", "password": "Admin@2026"})
    assert response.status_code == 200
    assert response.json()["username"] == "admin"


def test_login_failure():
    response = client.post("/api/login", json={"username": "admin", "password": "errado"})
    assert response.status_code == 401


def test_demo_user_login_success():
    response = client.post("/api/login", json={"username": "mario", "password": "mario123@"})
    assert response.status_code == 200
    assert response.json()["username"] == "mario"


def test_create_health_unit_and_update():
    create_response = client.post(
        "/api/health-units",
        json={
            "name": "Hospital Provincial do Uíge",
            "unit_type": "Hospital",
            "municipality": "Uíge",
            "address": "Rua 1 de Maio",
            "contact": "925000000",
            "status": "active",
        },
    )
    assert create_response.status_code == 201
    unit = create_response.json()

    update_response = client.put(
        f"/api/health-units/{unit['id']}",
        json={
            "name": "Hospital Provincial do Uíge",
            "unit_type": "Hospital",
            "municipality": "Damba",
            "address": "Rua da Saúde",
            "contact": "925000001",
            "status": "active",
        },
    )
    assert update_response.status_code == 200
    assert update_response.json()["municipality"] == "Damba"


def test_create_patient_and_search():
    unique_name = f"Ana Maria Sousa {uuid4().hex[:6]}"
    unit_response = client.post(
        "/api/health-units",
        json={
            "name": f"Centro de Saúde Teste {uuid4().hex[:6]}",
            "unit_type": "Centro de Saúde",
            "municipality": "Caxito",
            "address": "Rua das Flores",
            "contact": "923000111",
            "status": "active",
        },
    )
    assert unit_response.status_code == 201
    unit_id = unit_response.json()["id"]

    payload = {
        "full_name": unique_name,
        "birth_date": "1992-06-10",
        "gender": "Feminino",
        "identity_card": "000123456LA041",
        "nif": "900123456",
        "contact": "923456789",
        "address": "Rua das Flores, Uíge",
        "health_unit_id": unit_id,
    }
    create_response = client.post("/api/patients", json=payload)
    assert create_response.status_code == 201
    patient = create_response.json()
    assert patient["full_name"] == unique_name
    assert patient["patient_identifier"].startswith("PAT-")

    search_response = client.get("/api/patients", params={"query": unique_name.split()[0]})
    assert search_response.status_code == 200
    assert any(item["full_name"] == unique_name for item in search_response.json())


def test_create_consultation():
    unique_name = f"Paciente Consulta {uuid4().hex[:6]}"
    unit_response = client.post(
        "/api/health-units",
        json={
            "name": f"Hospital de Consulta {uuid4().hex[:6]}",
            "unit_type": "Hospital",
            "municipality": "Uíge",
            "address": "Rua do Atendimento",
            "contact": "923456700",
            "status": "active",
        },
    )
    unit_id = unit_response.json()["id"]
    patient_response = client.post(
        "/api/patients",
        json={
            "full_name": unique_name,
            "birth_date": "1988-03-21",
            "gender": "Masculino",
            "identity_card": "ABC987654",
            "nif": "123456789",
            "contact": "923123456",
            "address": "Rua da Consulta",
            "health_unit_id": unit_id,
        },
    )
    assert patient_response.status_code == 201

    consultation_response = client.post(
        "/api/consultations",
        json={
            "patient_id": patient_response.json()["id"],
            "professional_name": "Dra. Aline Ndalamba",
            "health_unit_id": unit_id,
            "consultation_datetime": "2026-11-10T09:30:00",
            "diagnosis": "Consulta de rotina",
            "observations": "Paciente está estável.",
        },
    )
    assert consultation_response.status_code == 201
    assert consultation_response.json()["diagnosis"] == "Consulta de rotina"


def test_get_patient_history():
    unique_name = f"Paciente Historico {uuid4().hex[:6]}"
    unit_response = client.post(
        "/api/health-units",
        json={
            "name": f"Centro Histórico {uuid4().hex[:6]}",
            "unit_type": "Centro de Saúde",
            "municipality": "Nzeto",
            "address": "Rua do Histórico",
            "contact": "923111222",
            "status": "active",
        },
    )
    unit_id = unit_response.json()["id"]
    patient_response = client.post(
        "/api/patients",
        json={
            "full_name": unique_name,
            "birth_date": "1975-02-14",
            "gender": "Feminino",
            "identity_card": "XYZ654321",
            "nif": "987654321",
            "contact": "923777888",
            "address": "Rua da História",
            "health_unit_id": unit_id,
        },
    )
    assert patient_response.status_code == 201
    patient_id = patient_response.json()["id"]

    consultation_response = client.post(
        "/api/consultations",
        json={
            "patient_id": patient_id,
            "professional_name": "Dr. António Muanza",
            "health_unit_id": unit_id,
            "consultation_datetime": "2026-11-11T10:00:00",
            "diagnosis": "Acompanhamento de rotina",
            "observations": "Paciente referiu melhoria geral após tratamento.",
        },
    )
    assert consultation_response.status_code == 201

    history_response = client.get(f"/api/patients/{patient_id}/history")
    assert history_response.status_code == 200
    payload = history_response.json()
    assert payload["patient"]["full_name"] == unique_name
    assert len(payload["consultations"]) >= 1
    assert payload["consultations"][0]["diagnosis"] == "Acompanhamento de rotina"
