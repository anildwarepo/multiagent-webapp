FROM python:3.10

RUN apt-get update \
    && apt-get install -y --no-install-recommends unixodbc-dev g++ \
    && curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY . /app/

RUN rm -rf /app/__pycache__
RUN rm Dockerfile

RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=multiagent_api.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

