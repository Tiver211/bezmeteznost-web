FROM python:3.11-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /api

EXPOSE 80

CMD ["bash", "api/start_workers.sh"]