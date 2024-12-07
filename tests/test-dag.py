import os
import logging
from contextlib import contextmanager
import pytest
from airflow.models import DagBag

# Context manager para deshabilitar temporalmente los logs de Airflow
@contextmanager
def suppress_logging(namespace):
    logger = logging.getLogger(namespace)
    old_value = logger.disabled
    logger.disabled = True
    try:
        yield
    finally:
        logger.disabled = old_value


# Función para capturar errores de importación
def get_import_errors():
    """
    Genera una lista de errores de importación en el DAGBag
    """
    with suppress_logging("airflow"):
        dag_bag = DagBag(include_examples=False)

        def strip_path_prefix(path):
            return os.path.relpath(path, os.environ.get("AIRFLOW_HOME"))

        return [(None, None)] + [
            (strip_path_prefix(k), v.strip()) for k, v in dag_bag.import_errors.items()
        ]


# Función para obtener todos los DAGs
def get_dags():
    """
    Genera una lista de (dag_id, DAG object, file location) del DAGBag
    """
    with suppress_logging("airflow"):
        dag_bag = DagBag(include_examples=False)

    def strip_path_prefix(path):
        return os.path.relpath(path, os.environ.get("AIRFLOW_HOME"))

    return [(k, v, strip_path_prefix(v.fileloc)) for k, v in dag_bag.dags.items()]


# Prueba 1: Errores de importación
@pytest.mark.parametrize(
    "rel_path, rv", get_import_errors(), ids=[x[0] for x in get_import_errors()]
)
def test_file_imports(rel_path, rv):
    """Verifica errores de importación en los archivos de DAGs"""
    if rel_path and rv:
        raise Exception(f"{rel_path} falló al importar con el siguiente error: \n{rv}")


# Prueba 2: Tags en los DAGs
APPROVED_TAGS = {"ventas360", "etl", "snowflake"}  # Tags permitidos para el proyecto Ventas360

@pytest.mark.parametrize(
    "dag_id, dag, fileloc", get_dags(), ids=[x[2] for x in get_dags()]
)
def test_dag_tags(dag_id, dag, fileloc):
    """
    Verifica si cada DAG tiene tags y si los tags son válidos
    """
    assert dag.tags, f"El DAG '{dag_id}' en {fileloc} no tiene tags definidos."
    assert set(dag.tags).issubset(APPROVED_TAGS), f"El DAG '{dag_id}' en {fileloc} tiene tags no aprobados: {dag.tags}"


# Prueba 3: Retries en los DAGs
@pytest.mark.parametrize(
    "dag_id, dag, fileloc", get_dags(), ids=[x[2] for x in get_dags()]
)
def test_dag_retries(dag_id, dag, fileloc):
    """
    Verifica que cada DAG tenga configurado 'retries' en default_args >= 2
    """
    retries = dag.default_args.get("retries", 0)
    assert (
        retries >= 2
    ), f"El DAG '{dag_id}' en {fileloc} debe tener 'retries' configurado como >= 2. Actualmente tiene: {retries}"
