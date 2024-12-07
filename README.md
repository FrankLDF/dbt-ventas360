# Project Ventas360 🚀

**Ventas360** is a data pipeline developed as part of a university project to manage and analyze sales data. It leverages the following modern tools for an efficient and scalable ETL workflow:

- **Snowflake**: Data storage and processing.
- **dbt**: Data modeling and transformation.
- **Airflow**: Task orchestration.

---

## 🛠️ Tools and Technologies Used

1. **Snowflake**: Cloud-based database for data storage.
2. **dbt (Data Build Tool)**: Tool for transforming data and creating SQL models.
3. **Airflow**: Workflow orchestrator for ETL processes.
4. **Python**: Main language for Airflow scripts.

---

## 📋 Pipeline Overview

1. **Extraction**:

   - Data is loaded and stored in **Snowflake**.

2. **Transformation**:

   - **dbt** is used to model and transform the data into clean, analysis-ready tables.

3. **Orchestration**:
   - **Airflow** coordinates the pipeline tasks, ensuring that extraction, transformation, and loading occur sequentially and automatically.

---

## 📦 Project Structure

```plaintext
ventas360/
│
├── airflow/               # Airflow configuration and DAGs
│   ├── dags/
│   │   └── ventas_pipeline.py
│   └── requirements.txt   # Required libraries for Airflow
│
├── dbt/                   # dbt project
│   ├── models/            # dbt SQL models
│   ├── profiles.yml       # Connection configuration for Snowflake
│   └── dbt_project.yml    # General project configuration
│
└── README.md              # Project documentation
```

🚀 Setup and Installation

1. Configure Snowflake

- Create a Snowflake account.
- Set up a database and schema to store sales data.
- Add credentials in the profiles.yml file for dbt.

📊 Pipeline Execution

1. Airflow triggers the main DAG.
2. Data is extracted and loaded into Snowflake.
3. dbt transforms the data using SQL models.
4. The processed data is ready for analysis.

👨‍💻 Author

- Name: Frank Luis Duarte
- Enrollment: 2021-0226
