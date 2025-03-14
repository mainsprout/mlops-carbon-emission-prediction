from typing import List
from datetime import datetime

from airflow import DAG
from airflow.models import Variable
from airflow.decorators import task
from airflow.models.param import Param
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

from support.date_values import DateValues, DateFormat

conn_id = "feature_store"
airflow_dags_path = Variable.get("AIRFLOW_DAGS_PATH")
# airflow_dags_path = "/home/mlops/Study/mlops-project-pipeline"
sql_file_path = f"{airflow_dags_path}/features/exam_data_generator/recipes/create_exam_data.sql"


def read_sql_file(file_path):
    with open(file_path, 'r') as file:
        sql_query_lines = file.read()
    return "".join(sql_query_lines)


def validate_exam_date(date_list, start_day, end_day):
    # Set the date and time range for validation
    exam_date_list = DateValues.get_datetime_list("202401180000", "202409270910")
    subtract_date_list = list(set(date_list) - set(exam_date_list))
    subtract_date_list.sort()
    # 수정된 조건문
    if len(subtract_date_list) > 0:
        raise ValueError("The data for the date range from 2024-01-11 11:00 to 2024-09-27 09:10 "
                         "is crucial for generating exam data. "
                         "Ensure that start and end dates are within this range.\n"
                         f"The dates you entered are: start_day = {start_day}, end_day = {end_day}")


@task(task_id="DATE_PARAMS")
def get_date_params(start_day, end_day) -> List:
    print(f"start_day = {start_day}")
    print(f"end_day = {end_day}")
    date_params = []
    date_list = DateValues.get_datetime_list(start_day, end_day)  # Adjust to handle datetime format
    validate_exam_date(date_list=date_list, start_day=start_day, end_day=end_day)
    for _datetime in date_list:
        date_params.append({"base_day": _datetime})
    print(f"date_params = {date_params}")
    return date_params


with DAG(dag_id="exam_data_generator",
         default_args={
             "owner": "mlops.study",
             "depends_on_past": False,
             "email": ["mlops.study@gmail.com"]
         },
         description="실습_데이터_생성",
         schedule=None,
         # start_date=datetime(2024, 12, 10),
         start_date = datetime.now(),
         catchup=False,
         tags=["mlops", "study"],
         params={
             "start_day": Param(
                 default="202401180000",
                 type="string",
                 minLength=12,
                 maxLength=12,
             ),
             "end_day": Param(
                 default="202409270910",
                 type="string",
                 minLength=12,
                 maxLength=12,
             )
         }
         ) as dag:
    data_generate = SQLExecuteQueryOperator.partial(
        task_id="실습_데이터_생성",
        conn_id=conn_id,
        sql=read_sql_file(sql_file_path),
        split_statements=True
    ).expand(
        params=get_date_params(start_day="{{ params.start_day }}",
                               end_day="{{ params.end_day }}")
    )
