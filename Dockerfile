#Usa uma imagem base do Python
FROM python:3.12.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cach-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "run.py"]