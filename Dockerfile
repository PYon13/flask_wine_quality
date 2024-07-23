FROM python:3.9
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
EXPOSE 5000
ENV FLASK_APP=start_app.py
ENV FLASK_ENV=prod_3_project
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]