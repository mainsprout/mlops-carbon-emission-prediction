import unittest
from airflow.utils.timezone import datetime
from tests import context
import os
from airflow.models import Variable

os.environ["FEATURE_STORE_URL"] = f"mysql://root:root@127.0.0.1:3307/mlops_project"
airflow_dags_path = Variable.get("AIRFLOW_DAGS_PATH")
os.environ["MODEL_OUTPUT_HOME"] = (f"{airflow_dags_path}"
                                   f"/models/traffic_model")
home_dir = os.path.expanduser("/home/mlops")
os.environ["MLOPS_DATA_STORE"] = f"{home_dir}/airflow/mlops_data_store"

class TestTrafficModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
      # Common Given
      cls.base_day = datetime(2024, 2, 2).strftime("%Y%m%d")
      cls.context = context


    def test_data_extract(self):
      print(home_dir)
      # Given
      import models.traffic_model.traffic_model as model

      # When
      model.data_extract.__setattr__(
          'sql',
          model.read_sql_file(model.sql_file_path).replace(
              '20240202',
              self.base_day
          )
      )
      model.data_extract.execute(self.context)


    def test_data_preparation(self):
      # Given
      import models.traffic_model.traffic_model as model
      from models.traffic_model.data_preparation.preparation import \
        Preparation

      # When
      preparation = Preparation(model_name=model.model_name,
                                model_version=model.model_version,
                                base_day=self.base_day)
      preparation.preprocessing()


    def test_data_preparation_of_dag_task(self):
      import models.traffic_model.traffic_model as model
      env = {"PYTHON_FILE": "/home/mlops/model/preparation.py",
             "MODEL_NAME": model.model_name,
             "MODEL_VERSION": model.model_version,
             "BASE_DAY": self.base_day}
      # ineligible_loan_model.py DAG파일에 작성된 data_preparation Task의 BashOperator에 사용되는
      # env 매개변수의 인수를 변경하기 위해서 __setattr__ 함수에 테스트 케이스용 env를 입력한다.
      model.data_preparation.__setattr__("env", env)
      # data_preparation Task를 실행하면, 테스트 케이스용 env로 치환되어 실행됨.
      model.data_preparation.execute(self.context)


    def test_prediction(self):
      import models.traffic_model.traffic_model as model
      from models.traffic_model.model.prediction import Prediction

      # When
      prediction = Prediction(model_name=model.model_name,
                              model_version=model.model_version,
                              base_day=self.base_day)
      prediction.predict()


    def test_prediction_of_dag_task(self):
      import models.traffic_model.traffic_model as model
      env = {"PYTHON_FILE": "/home/mlops/model/prediction.py",
             "MODEL_NAME": model.model_name,
             "MODEL_VERSION": model.model_version,
             "BASE_DAY": self.base_day}
      model.prediction.__setattr__("env", env)
      model.prediction.execute(self.context)