#Usa uma imagem base do Python
FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "run.py"]