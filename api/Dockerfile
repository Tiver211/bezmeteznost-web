FROM python:3.11-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /api

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "api.app:app"]
