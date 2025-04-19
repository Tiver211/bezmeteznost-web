FROM python:3.11-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /api

EXPOSE 80
CMD ["uvicorn", "api.app:app", "--port", "80", "--host=0.0.0.0"]