import pendulum
from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from support.callback_functions import success_callback, failure_callback
import os

local_timezone = pendulum.timezone("Asia/Seoul")
conn_id = "feature_store"
model_name = "traffic_model"
model_version = "1.0.0"
airflow_dags_path = Variable.get("AIRFLOW_DAGS_PATH")
# airflow_dags_path = "/home/mlops/Study/mlops-project-pipeline"
sql_file_path = (f"{airflow_dags_path}/models/traffic_model"
                 f"/data_extract/features.sql")

def read_sql_file(file_path):
  with open(file_path, 'r') as file:
      sql_query_lines = file.read()
  return "".join(sql_query_lines)

with DAG(dag_id="traffic_model",
         default_args={
           "owner": "mlops.study",
           "depends_on_past": False,
           "email": ["mlops.study@gmail.com"],
           "on_failure_callback": failure_callback,
           "on_success_callback": success_callback,
         },
         description="교통패턴분석모델",
         schedule="0 4 * * *",
         # start_date=datetime(2024,9,26, tzinfo=local_timezone),
         start_date=datetime.now(local_timezone),
         catchup=False,
         tags=["mlops", "study"]
        ) as dag:
    # data_extract = EmptyOperator(task_id="데이터추출")
    data_extract = SQLExecuteQueryOperator(
        task_id="데이터_추출",
        conn_id=conn_id,
        sql=read_sql_file(sql_file_path),
        split_statements=True
    )

    # data_preparation = EmptyOperator(task_id="데이터전처리")
    data_preparation = BashOperator(
        task_id="데이터전처리",
        # cd 명령어로 docker-compose.yml 파일이 존재하는 디렉터리 위치로 이동
        # docker-compose up 명령어를 실행하여 데이터 전처리 코드를 실행, 그리고 --build 옵션을 추가하여
        # 항상 코드의 변경이 있으면 새로운 이미지를 생성하고 실행함.
        # 컨테이너의 작업이 종료되면, docker-compose down 컨테이너를 중지시키고 컨테이너를 삭제함.
        bash_command=f"cd {airflow_dags_path}/models/traffic_model/docker && "
                     "docker-compose up --build && docker-compose down",
        env={"PYTHON_FILE": "/mlops/home/Study/mlops-project-pipeline/models/traffic_model/data_preparation/preparation.py",
             "MODEL_NAME": model_name,
             "MODEL_VERSION": model_version,
             # "BASE_DAY": "{{ yesterday_ds_nodash }}"
             "BASE_DAY": "20240202"
             },
        append_env=True,
        retries=1,
    )


    prediction = BashOperator(
        task_id="예측",
        bash_command=f"cd {airflow_dags_path}/models/traffic_model/docker && "
                      "docker-compose up --build && docker-compose down",
        env={"PYTHON_FILE": "/home/mlops/model/prediction.py",
             "MODEL_NAME": model_name,
             "MODEL_VERSION": model_version,
             # "BASE_DAY": "{{ yesterday_ds_nodash }}",
             "BASE_DAY": "20240202"},
        append_env=True, # 시스템 환경변수에 env가 반영되도록 한다.
        retries=1
    )


    data_extract >> data_preparation >> prediction