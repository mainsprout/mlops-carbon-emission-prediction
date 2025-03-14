import pendulum
from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from support.callback_functions import success_callback, failure_callback

local_timezone = pendulum.timezone("Asia/Seoul")
conn_id = "feature_store"
model_name = "traffic_model"
# airflow_dags_path = "/home/mlops/Study/mlops-project-pipeline"
airflow_dags_path = Variable.get("AIRFLOW_DAGS_PATH")
sql_file_path = f"{airflow_dags_path}/models" \
                f"/traffic_model_ct/data_extract/features.sql"

def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        sql_query_lines = file.read()
    return "".join(sql_query_lines)


with DAG(dag_id="traffic_model_ct",
         default_args={
           "owner": "mlops.study",
           "depends_on_past": False,
           "email": ["mlops.study@gmail.com"],
           "on_failure_callback": failure_callback,
           "on_success_callback": success_callback,
         },
         description="교통패턴분석모델CT",
         schedule=None,
         start_date=datetime(2024, 6, 23, tzinfo=local_timezone),
         # start_date=datetime.now(local_timezone),
         catchup=False,
         tags=["mlops", "study"],
         ) as dag:
  data_extract = SQLExecuteQueryOperator(
      task_id="데이터추출",
      conn_id=conn_id,
      sql=read_sql_file(sql_file_path),
      split_statements=True
  )

  data_preparation = BashOperator(
      task_id="데이터전처리",
      bash_command=f"cd {airflow_dags_path}/models/traffic_model_ct/docker && "
                   "docker-compose up --build && docker-compose down",
      env={"PYTHON_FILE": "/home/mlops/data_preparation/preparation.py",
           "MODEL_NAME": model_name,
           # "BASE_DAY": "{{ ds_nodash }}"
           "BASE_DAY": "20240622"
           },
      append_env=True,
      retries=1,
  )

  training = BashOperator(
      task_id="모델학습및모델평가",
      bash_command=f"cd {airflow_dags_path}/models/traffic_model_ct/docker && "
                   "docker-compose up --build && docker-compose down",
      env={"PYTHON_FILE": "/home/mlops/model/training.py",
           "MODEL_NAME": model_name,
           # "BASE_DAY": "{{ ds_nodash }}"
           "BASE_DAY": "20240622"
           },
      append_env=True,
      retries=1,
  )

  cd = TriggerDagRunOperator(task_id="지속적배포실행",
                             trigger_dag_id="traffic_model_cd",
                             allowed_states=["success"])

  data_extract >> data_preparation >> training >> cd