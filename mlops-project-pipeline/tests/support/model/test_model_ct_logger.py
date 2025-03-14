import os
import unittest

os.environ['FEATURE_STORE_URL'] = \
  f"mysql://root:root@127.0.0.1:3307/mlops_project"


class TestModelCtLogger(unittest.TestCase):

  @classmethod
  def setUpClass(cls) -> None:
      from support.model.model_ct_logger import ModelCtLogger
      model_name = "traffic_model"
      model_version = "1.0.1"
      cls.model_ct_logger = ModelCtLogger(model_name=model_name,
                                          model_version=model_version)

# 학습 기준일의 cutoff_date를 self.model_ct_logger.logging_started() 함수에 인수로
# 넘겨 지속적 학습 시작 로깅을 하는 함수를 테스트
  def test_01_logging_started(self):
      cutoff_date = "202412"
      self.model_ct_logger.logging_started(cutoff_date=cutoff_date)

# logging_started() 함수를 호출하여 모델의 지속적 학습을 종료하는 로깅 기능과
# 성능 지표를 저장하는 기능을 테스트한다.
  def test_02_logging_finished(self):
      metrics = {"accuracy": 90.23211}
      self.model_ct_logger.logging_finished(metrics=metrics)

  def test_03_get_training_cutoff_date(self):
    training_cutoff_date = \
      self.model_ct_logger.get_training_cutoff_date()
    print(f"training_cutoff_date = {training_cutoff_date}")