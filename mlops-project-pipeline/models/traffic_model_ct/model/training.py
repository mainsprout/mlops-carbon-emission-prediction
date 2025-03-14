import os
import sys
import joblib
import pandas as pd

mlops_data_store = os.getenv('MLOPS_DATA_STORE', "")
# mlops_data_store = "/home/mlops/airflow/mlops_data_store"

class Training:
    def __init__(self,
                 model_name: str,
                 model_version: str,
                 base_day: str):
        self._model_name = model_name
        self._model_version = model_version
        self._base_day = base_day
        self._data_preparation_path = f"{mlops_data_store}/data_preparation" \
                                      f"/{self._model_name}/ct/{self._base_day}"
        self._model_output_path = f"{mlops_data_store}/model/{self._model_name}" \
                                  f"/{self._model_version}/{self._base_day}"
        self._makedir()

    def _makedir(self):
        if not os.path.isdir(self._model_output_path):
            os.makedirs(self._model_output_path)

    def train(self):
        metrics = {}

        # 데이터 로드
        traffic_df = pd.read_csv(
            f"{self._data_preparation_path}/{self._model_name}.csv")
        print(f"{self._data_preparation_path}/{self._model_name}.csv")
        print(f"len(traffic_df): {len(traffic_df)}")

        from support.model.evaluation.lift import Lift
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import mean_squared_error, r2_score
        import xgboost as xgb

        # 특징 및 타겟 정의
        features = list(traffic_df.columns)
        target = 'vol'

        if target not in features:
            raise ValueError(f"Target column '{target}' is not in the dataset.")

        features.remove(target)
        x = traffic_df[features]
        y = traffic_df[target]

        # 데이터 분할
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2,
                                                            random_state=42)

        # XGBoost 데이터셋 준비
        dtrain = xgb.DMatrix(x_train, label=y_train)
        dtest = xgb.DMatrix(x_test, label=y_test)

        # 모델 파라미터 설정
        params = {
            'objective': 'reg:squarederror',
            'max_depth': 3,
            'learning_rate': 0.1,
        }

        # 모델 학습
        xgb_model = xgb.train(params, dtrain, num_boost_round=100)

        # 예측
        train_predict = xgb_model.predict(dtrain)
        test_predict = xgb_model.predict(dtest)

        # 성능 평가
        train_mse = mean_squared_error(y_train, train_predict)
        test_mse = mean_squared_error(y_test, test_predict)
        train_r2 = r2_score(y_train, train_predict)
        test_r2 = r2_score(y_test, test_predict)

        print(f"Train MSE: {train_mse}")
        print(f"Test MSE: {test_mse}")
        print(f"Train R2 Score: {train_r2}")
        print(f"Test R2 Score: {test_r2}")

        metrics["train"] = {
            "mse": train_mse,
            "r2_score": train_r2
        }
        metrics["test"] = {
            "mse": test_mse,
            "r2_score": test_r2
        }

        # 모델 저장
        model_file_name = f"{self._model_name}.joblib"
        joblib.dump(xgb_model, f"{self._model_output_path}/{model_file_name}")

        # 테스트 결과 저장
        test_results = pd.DataFrame({
            'datetime': traffic_df.loc[x_test.index, 'datetime'],
            'vol': y_test,
            'pasng_spd': traffic_df.loc[x_test.index, 'pasng_spd'],
            'predicted_vol': test_predict
        })

        output_file_name = f"{self._model_name}_test_results.csv"
        test_results.to_csv(f"{self._model_output_path}/{output_file_name}",
                            index=False)

        # 테스트 결과를 metrics에 저장
        metrics["test_results"] = test_results.to_dict(orient="list")

        print(f"Model saved to {model_file_name}")
        print(f"Test results saved to {output_file_name}")
        print(f"Metrics: {metrics}")

        return metrics


if __name__ == "__main__":
    print(f"sys.argv = {sys.argv}")
    if len(sys.argv) != 3:
        print("Insufficient arguments.")
        sys.exit(1)

    from support.date_values import DateValues
    from support.model.model_version import ModelVersion
    from support.model.model_ct_logger import ModelCtLogger

    _model_name = sys.argv[1]
    _base_day = sys.argv[2]
    _model_version = \
        ModelVersion(model_name=_model_name).get_next_ct_model_version()
    _base_ym = DateValues().get_before_one_day(_base_day)

    print(f"_model_name = {_model_name}")
    print(f"_base_day = {_base_day}")
    print(f"_model_version = {_model_version}")
    print(f"_base_ym = {_base_ym}")

    _ct_logger = ModelCtLogger(model_name=_model_name,
                               model_version=_model_version)
    _ct_logger.logging_started(cutoff_date=_base_ym)
    training = Training(model_name=_model_name,
                        model_version=_model_version,
                        base_day=_base_ym)
    _metrics = training.train()
    _ct_logger.logging_finished(metrics=_metrics)