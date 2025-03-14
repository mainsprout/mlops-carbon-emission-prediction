import os
import unittest
from airflow.models import Variable
from airflow.utils.timezone import datetime

from models.traffic_model.traffic_model import prediction
from support.date_values import DateValues
from tests import context

# airflow_dags_path = Variable.get("AIRFLOW_DAGS_PATH")
# home_dir = os.path.expanduser("/home/mlops")
home_dir = os.path.expanduser("~")
airflow_dags_path = Variable.get("AIRFLOW_DAGS_PATH")
os.environ['MLOPS_DATA_STORE'] = f"{home_dir}/airflow/mlops_data_store"
os.environ['MODEL_OUTPUT_HOME'] = f"{airflow_dags_path}/models/traffic_model"
os.environ['FEATURE_STORE_URL'] = \
  f"mysql+pymysql://root:root@127.0.0.1:3307/mlops_project"

class TestTrafficModel(unittest.TestCase):
    base_day = '20240623'

    @classmethod
    def setUpClass(cls) -> None:
        # Common Given
        # cls.base_day = DateValues().get_current_date() # 당일
        cls.start_date = '2024'
        cls.base_dt = DateValues().get_before_one_day(cls.base_day) # 전일
        cls.context = context


    def test_data_extract(self):
        import models.traffic_model_ct.traffic_model_ct as model

        # When
        model.data_extract.__setattr__('sql',
                                       model.read_sql_file(model.sql_file_path)
                                       .replace('{{ ds_nodash }}',
                                        self.base_day))
        model.data_extract.execute(self.context)


    def test_data_preparation(self):
        import models.traffic_model_ct.traffic_model_ct as model
        from models.traffic_model_ct.data_preparation.preparation import \
          Preparation

        # When
        preparation = Preparation(model_name=model.model_name,
                                  base_day=self.base_dt)
        preparation.preprocessing()


    def test_training(self):
        # Given
        import models.traffic_model_ct.traffic_model_ct as model
        from models.traffic_model_ct.model.training import Training
        ct_model_version = "1.0.0"

        # When
        training = Training(model_name=model.model_name,
                            model_version=ct_model_version,
                            base_day=self.base_dt)
        training.train()