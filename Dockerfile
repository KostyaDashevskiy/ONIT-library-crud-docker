# Стейдж 1: Сборка зависимостей (Builder)
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
# Устанавливаем зависимости в локальную папку
RUN pip install --user -r requirements.txt

# Стейдж 2: Финальный образ (Runner)
FROM python:3.11-slim as runner
WORKDIR /app

# Устанавливаем curl для healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Копируем зависимости из первого стейджа
COPY --from=builder /root/.local /root/.local
# Копируем код приложения
COPY . .

# Добавляем установленные пакеты в PATH
ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]