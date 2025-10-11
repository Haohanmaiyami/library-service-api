import pytest

@pytest.mark.django_db
def test_openapi_schema_and_docs(api):
    assert api.get("/api/schema/").status_code == 200
    #  тот маршрут, который выставил в urls.py
    docs = api.get("/api/docs/")
    if docs.status_code == 404:
        docs = api.get("/api/redoc/")
    assert docs.status_code == 200