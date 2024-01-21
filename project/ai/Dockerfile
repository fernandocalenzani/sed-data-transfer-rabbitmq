FROM python:3.10

WORKDIR /ai

COPY requirements.txt /ai/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /ai/

CMD ["python", "__main.py"]
