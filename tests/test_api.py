from fastapi.testclient import TestClient

from src.config_validator.api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_validate_endpoint_config_valido():
    payload = {
        "config": "interface GigabitEthernet0/1\n switchport access vlan 10\n ip address 192.168.0.1/24"
    }
    response = client.post("/validate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is True


def test_validate_endpoint_config_invalido():
    payload = {"config": "switchport access vlan 9000"}
    response = client.post("/validate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["valid"] is False
    assert body["errors"][0]["type"] == "vlan"
