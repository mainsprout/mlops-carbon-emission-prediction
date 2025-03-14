import pendulum
from datetime import datetime
from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from support.callback_functions import success_callback, failure_callback
import os

local_timezone = pendulum.timezone("Asia/Seoul")
os.environ["AIRFLOW_CONN_FEATURE_STORE"] = "mysql://root:root@127.0.0.1:3307/mlops_project"

conn_id = "feature_store"

with DAG(
    dag_id="data_extract_pipeline",
    default_args={
        "owner": "mlops.study",
        "depends_on_past": False,
        "email": ["mlops.study@gmail.com"],
        "on_failure_callback": failure_callback,
        "on_success_callback": success_callback,
        "timezone": local_timezone,
    },
    description="데이터추출_파이프라인",
    schedule_interval=None,
    # start_date=datetime(2024, 9, 26, tzinfo=local_timezone),
    start_date=datetime.now(local_timezone),
    catchup=False,
    tags=["mlops", "study"],
) as dag:
    task1_sql = """
        create database if not exists temp
    """
    task1 = SQLExecuteQueryOperator(
        task_id="create_database_temp",
        conn_id=conn_id,
        sql=task1_sql,
    )

    task2_sql = """
        drop table if exists temp.traffic_model_features
    """
    task2 = SQLExecuteQueryOperator(
        task_id="drop_table_temp_traffic_model_features",
        conn_id=conn_id,
        sql=task2_sql,
    )

    task3_sql = """
        create table temp.traffic_model_features as
        select creat_de, creat_hm, std_link_id, vol, pasng_spd
        from mlops_project.area
        limit 8000
    """
    task3 = SQLExecuteQueryOperator(
        task_id="create_table_temp_traffic_model_features",
        conn_id=conn_id,
        sql=task3_sql,
    )


    task4_sql = """
        create table if not exists mlops_project.traffic_model_features (
            creat_de VARCHAR(8),
            creat_hm VARCHAR(4),
            std_link_id VARCHAR(10),
            vol BIGINT(15),
            pasng_spd DECIMAL(5,2)
        )
    """
    task4 = SQLExecuteQueryOperator(
        task_id="create_table_mlops_project_traffic_model_features",
        conn_id=conn_id,
        sql=task4_sql,
    )

    task5_sql = """
        insert into mlops_project.traffic_model_features (creat_de, creat_hm, std_link_id, vol, pasng_spd)
        select creat_de, creat_hm, std_link_id, vol, pasng_spd
        from temp.traffic_model_features
    """
    task5 = SQLExecuteQueryOperator(
        task_id="insert_into_mlops_project_traffic_model_features",
        conn_id=conn_id,
        sql=task5_sql,
    )

    task1 >> task2 >> task3 >> task4 >> task5
