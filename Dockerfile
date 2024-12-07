
FROM quay.io/astronomer/astro-runtime:12.4.0


WORKDIR /usr/local/airflow


RUN python -m venv dbt_venv && \
    source dbt_venv/bin/activate && \
    pip install --no-cache-dir dbt-snowflake==1.7.0 && \
    deactivate


COPY dags/ ./dags/
COPY dbt/ ./dbt/            # Copia los archivos de dbt (si los tienes)
COPY requirements.txt ./requirements.txt


RUN pip install --no-cache-dir -r requirements.txt


ENV AIRFLOW_HOME=/usr/local/airflow
ENV PATH="$PATH:/usr/local/airflow/dbt_venv/bin"

CMD ["bash", "-c", "airflow db init && airflow scheduler & airflow webserver"]
