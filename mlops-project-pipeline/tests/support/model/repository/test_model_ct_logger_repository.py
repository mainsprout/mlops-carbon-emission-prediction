import os
import json
import unittest


os.environ['FEATURE_STORE_URL'] = \
  f"mysql://root:root@127.0.0.1:3307/mlops_project"


class TestModelCtLoggerRepository(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from support.model.repository.model_ct_logger_repository import (
            ModelCtLoggerRepository
        )
        cls.model_name = 'traffic_model'
        cls.model_version = "1.0.1"
        cls.model_ct_logger_repository = ModelCtLoggerRepository()

    def test_01_logging_init(self):
        self.model_ct_logger_repository. \
            logging_init(model_name=self.model_name,
                         model_version=self.model_version)

    # 모델의 지속적 학습을 시작하는 로깅 기능을 테스트
    def test_02_logging_started(self):
        cutoff_date = "202408"
        self.model_ct_logger_repository. \
            logging_started(model_name=self.model_name,
                            model_version=self.model_version,
                            cutoff_date=cutoff_date)

    def test_03_logging_finished(self):
        metrics = json.dumps({"accuracy": 87.12314})
        self.model_ct_logger_repository. \
            logging_finished(model_name=self.model_name,
                             model_version=self.model_version,
                             metrics=metrics)

    def test_04_get_training_cutoff_date(self):
        training_cutoff_date = self.model_ct_logger_repository. \
            get_training_cutoff_date(model_name=self.model_name,
                                     model_version=self.model_version)
        print(f"training_cutoff_date = {training_cutoff_date}")