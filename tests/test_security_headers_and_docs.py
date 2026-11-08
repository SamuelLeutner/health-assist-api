import pytest
from fastapi.testclient import TestClient

EXPECTED_SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Content-Security-Policy": "default-src 'none'",
    "Referrer-Policy": "no-referrer",
}

DOCUMENTED_OPERATIONS = {
    ("get", "/health"),
    ("post", "/auth/token"),
    ("post", "/predict/"),
    ("get", "/predict/{log_id}"),
}


@pytest.mark.parametrize("path", ["/health", "/predict/1"], ids=["ok", "error-401"])
def test_security_headers_are_present_on_every_response(
    client: TestClient, path: str
):
    response = client.get(path)

    for header, expected in EXPECTED_SECURITY_HEADERS.items():
        assert response.headers[header] == expected
    assert "max-age=" in response.headers["Strict-Transport-Security"]


def test_swagger_ui_is_accessible(client: TestClient):
    response = client.get("/docs")

    assert response.status_code == 200
    assert "swagger-ui" in response.text.lower()


def test_openapi_documents_every_endpoint_with_input_and_output_schemas(
    client: TestClient,
):
    spec = client.get("/openapi.json").json()

    documented = {
        (method, path) for path, ops in spec["paths"].items() for method in ops
    }
    assert documented == DOCUMENTED_OPERATIONS

    for method, path in DOCUMENTED_OPERATIONS:
        operation = spec["paths"][path][method]
        success = operation["responses"]["200"]["content"]["application/json"]
        assert "schema" in success, f"{method.upper()} {path} sem schema de saída"

    for method, path in {("post", "/auth/token"), ("post", "/predict/")}:
        assert "requestBody" in spec["paths"][path][method], (
            f"{method.upper()} {path} sem schema de entrada"
        )