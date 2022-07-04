FROM python:3.9-slim

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8050

CMD ["python", "app.py"]