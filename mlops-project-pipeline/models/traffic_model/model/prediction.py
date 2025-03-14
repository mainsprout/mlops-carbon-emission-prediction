import xgboost as xgb
import os
import sys
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sqlalchemy import text

mlops_data_store = os.getenv("MLOPS_DATA_STORE", "")
# mlops_data_store = "/home/mlops/airflow/mlops_data_store"
model_output_home = os.getenv("MODEL_OUTPUT_HOME", "")
# model_output_home = "/home/mlops/Study/mlops-project-pipeline/models/traffic_model"
feature_store_url = os.getenv("FEATURE_STORE_URL", "")


class Prediction:
    def __init__(self,
                model_name: str,
                model_version: str,
                base_day: str):
        self._model_name = model_name
        self._model_version =  model_version
        self._base_day = base_day


    def predict(self):
        # 피처 불러오기
        feature_df = self._get_encoded_features()

        xgb_model = self._load_model()

        test_predicted = self._predict(feature_df, xgb_model)

        self._save_to_table(test_predicted)


    def _save_to_table(self, test_predicted):
      ####################################################################
      ## 5. 모델 예측 결과 저장
      ####################################################################
      from sqlalchemy import create_engine
      engine = create_engine(feature_store_url)
      with engine.connect() as conn:
        init_sql = text(f"""
                    delete
                      from mlops_project.traffic_model_result
                    where base_dt = '{self._base_day}'  
                    """)
        conn.execute(init_sql)
        insert_rows = test_predicted.to_sql(name="traffic_model_result",
                                            con=conn,
                                            schema="mlops_project",
                                            if_exists="append",
                                            index=False)
        print(f"insert_rows = {insert_rows}")


    def _predict(self, feature_df, xgb_model):

      print(feature_df.columns)
      # Feature와 Target 분리
      features = ['datetime', 'std_link_id', 'pasng_spd']
      target = 'vol'

      x = feature_df[features]
      y = feature_df[target]

      # Train-test split
      x_train, x_test, y_train, y_test = train_test_split(
          x, y, test_size=0.2, random_state=42
      )

      # DMatrix 변환
      dtrain = xgb.DMatrix(x_train, label=y_train)
      dtest = xgb.DMatrix(x_test, label=y_test)

      # 예측 수행
      train_predictions = xgb_model.predict(dtrain)
      test_predictions = xgb_model.predict(dtest)

      print("Target on train data (sample 20):", train_predictions[:20])
      print("Target on test data (sample 20):", test_predictions[:20])

      # test_data 생성
      test_data = {
          "base_dt": self._base_day,
          "datetime": x_test['datetime'].tolist(),
          "pasng_spd": x_test['pasng_spd'].tolist(),
          "std_link_id": x_test['std_link_id'].tolist(),
          "predict": test_predictions.tolist(),
      }

      # DataFrame으로 변환
      test_predicted = pd.DataFrame(data=test_data)

      # 결과 출력
      print("test_predicted", test_predicted)

      return test_predicted

    def _load_model(self):
      # 모델 불러오기
      model_file_name = f"{self._model_name}.joblib"
      xgb_model = joblib.load(f"{model_output_home}"
                                   f"/model_output/{model_file_name}")
      print(model_file_name)
      print(f"{model_output_home}"
                                   f"/model_output/{model_file_name}", "###")
      return xgb_model


    def _get_encoded_features(self):
      # data_preparation_data_path에 데이터 전처리 결과 데이터의 디렉터리 경로를 저장함.
      data_preparation_data_path = \
        f"{mlops_data_store}/data_preparation/{self._model_name}" \
        f"/{self._model_version}/{self._base_day}"
      feature_df = pd.read_csv(
          f"{data_preparation_data_path}"
          f"/{self._model_name}_{self._model_version}.csv"
      )

      return feature_df



if __name__ == "__main__":
    print(f"sys.argv = {sys.argv}")
    if len(sys.argv) != 4:
        print("Insufficient arguments.")
        sys.exit(1)

    _model_name = sys.argv[1]
    _model_version = sys.argv[2]
    _base_day = sys.argv[3]

    print(f"_model_name = {_model_name}")
    print(f"_model_version = {_model_version}")
    print(f"_base_day = {_base_day}")

    prediction = Prediction(model_name=_model_name,
                            model_version=_model_version,
                            base_day=_base_day)

    prediction.predict()