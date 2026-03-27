from fastapi.testclient import TestClient
from app import app, Base, engine

# Создаем чистые таблицы перед тестами
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_crud_workflow():
    # 1. Проверка Healthcheck
    response = client.get("/health")
    assert response.status_code == 200

    # 2. Создание (Create)
    response = client.post("/add", data={"title": "1984", "author": "George Orwell"})
    assert response.status_code == 200 # Redirect приводит на главную

    # 3. Чтение (Read)
    response = client.get("/")
    assert response.status_code == 200
    assert "1984" in response.text
    assert "George Orwell" in response.text

    # (Дальнейшие шаги Update и Delete можно добавить по аналогии)