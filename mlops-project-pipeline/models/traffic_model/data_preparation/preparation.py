import os
import pandas as pd
import joblib
import sys

feature_store_url = os.getenv("FEATURE_STORE_URL",
                              "mysql+pymysql://root:root@localhost:3307/mlops_project")
model_output_home = os.getenv("MODEL_OUTPUT_HOME", "")
# model_output_home = "/home/mlops/Study/mlops-project-pipeline/models/traffic_model"
mlops_data_store = os.getenv("MLOPS_DATA_STORE", "")

class Preparation:
  def __init__(self,
      model_name: str,
      model_version: str,
      base_day: str):
    self._model_name = model_name
    self._model_version = model_version
    self._base_day = base_day
    self._data_preparation_path = \
      (f"{mlops_data_store}/data_preparation/{self._model_name}"
       f"/{self._model_version}/{self._base_day}")  # 데이터 전처리된 데이터를 해당 위치에 저장할거임.
    self._makedir()

  def _makedir(self):
      if not os.path.isdir(self._data_preparation_path):
          os.makedirs(self._data_preparation_path)

  def preprocessing(self):
    traffic_df = self._get_features_extracted()
    self._fill_na_to_default(traffic_df)
    traffic_df = self._transform_to_label_encoding(traffic_df)
    numeric_features = self._transform_to_standard_scale(traffic_df)
    self._transform_to_min_max_scale(numeric_features, traffic_df)
    self._save_encoded_features(traffic_df)


  def _save_encoded_features(self, traffic_df):
    """
      피처 데이터 저장
      """
    feature_file_name = f"{self._model_name}_{self._model_version}.csv"
    traffic_df.to_csv(f"{self._data_preparation_path}"
                      f"/{feature_file_name}", index=False)


  @staticmethod
  def _transform_to_min_max_scale(numeric_features, traffic_df):
    # 'vol', 'pasng_spd' 피처 데이터로 각각 min_max_scaler를 훈련(fit)하고 min_max_scalers 딕셔너리에 저장
    # min/max scalers 학습(Fit)
    # 2. 표준화에서 사용했던 numeric_features 리스트의 각 수치형 피처명에 대해 반복문을 실행하고, 각 수치형 피처(numeric_feature)에 대한
    # 새로운 MinMaxScaler 객체를 생성한다. min_max_scaler.fit() 함수에 traffic_df[[numeric_feature]]의 피처값을 입력하여 스케일러를 학습하고
    # 그 결과를 min_max_saclers 딕셔너리에 저장.
    # min_max_scalers 불러오기
    min_max_scalers = joblib.load(f'{model_output_home}'
                                  f'/model_output/min_max_scalers.joblib')
    # numeric_features 정규화
    # 다시 numeric_features 리스트의 각 수치형 피처명에 대해 반복문을 실행하고, min_max_scaler.transform() 함수에 traffic_df[[numeric_feature]]
    # 피처값을 입력하여 수치형 피처의 원래 데이터를 Min-Max 스케일러를 사용하여 정규화하고, traffic_df 에 저장.
    print(f"numeric_features 정규화")
    for numeric_feature in numeric_features:
      min_max_scaler = min_max_scalers[numeric_feature]
      print(f"numeric_feature = {numeric_feature}")

      traffic_df[numeric_feature] = min_max_scaler.transform(
          traffic_df[[numeric_feature]])
    print("traffic_df 결과 저장 예정!!!")


  @staticmethod
  def _transform_to_standard_scale(traffic_df):
    numeric_features = ['pasng_spd']
    # standard scalers 학습(Fit)
    # numeric_features 리스트의 각 수치형 피처명에 대해 반복문을 실행하고, 각 수치형 피처(numeric_feature)에 대한 새로운 StandardScaler 개게를 생성
    # sandard_scalr.fit() 함수에 traffic_df[[numeric_feature]]의 피처값을 입력하여 스케일러를 학습하고, 그 결과를 standard_scalers 딕셔너리에 저장
    # standard_scalers 불러오기
    standard_scalers = joblib.load(f'{model_output_home}'
                                   f'/model_output/standard_scalers.joblib')
    # numeric_features 표준화
    # 다시 numeric_features 리스트의 각 수치형 피처명에 대해 반복문을 수행하고, standard_scaler, transform() 함수에 traffic_df[[numeric_feature]]
    # 피처값을 입력하여 수치형 피처의 원래 데이터를 표준 스케일러를 사용하여 표준화하고, traffic_df에 저장한다.
    for numeric_feature in numeric_features:
      standard_scaler = standard_scalers[numeric_feature]
      print(f"numeric_feature = {numeric_feature}")

      traffic_df[numeric_feature] = standard_scaler.transform(
          traffic_df[[numeric_feature]])
    return numeric_features


  @staticmethod
  def _transform_to_label_encoding(traffic_df):
    from sklearn.preprocessing import LabelEncoder

    # 라벨 인코딩
    label_encoder = LabelEncoder()
    traffic_df['std_link_id'] = label_encoder.fit_transform(traffic_df['std_link_id'])
    print(traffic_df[['std_link_id']].head())
    return traffic_df


  @staticmethod
  def _fill_na_to_default(traffic_df):
    traffic_df['std_link_id'].fillna(method='ffill', inplace=True)
    traffic_df['vol'].fillna(traffic_df['vol'].mean(), inplace=True)
    traffic_df['pasng_spd'].fillna(traffic_df['pasng_spd'].mean(), inplace=True)
    traffic_df['datetime'].fillna(method='ffill', inplace=True)


  @staticmethod
  def _get_features_extracted():
    from sqlalchemy import create_engine, text
    engine = create_engine(feature_store_url)
    ## 데이터 추출(01_data_extract.sql) 결과를 조회한다.
    sql = f"""
        select *
          from mlops_project.traffic_model_features
    """
    with engine.connect() as conn:
      traffic_df = pd.read_sql(text(sql), con=conn)

    # 디버깅 출력
    print(f"traffic_df.shape = {traffic_df.shape}")
    print(traffic_df.head())

    if traffic_df.empty:
      raise ValueError("traffic df is empty!")

    traffic_df['datetime'] = pd.to_datetime(
    traffic_df['creat_de'] + ' ' + traffic_df['creat_hm'])
    traffic_df['datetime'] = traffic_df['datetime'].dt.strftime('%Y%m%d%H%M')
    traffic_df['datetime'] = traffic_df['datetime'].astype('int64')
    traffic_df.drop(columns=['creat_de', 'creat_hm'], inplace=True)
    traffic_df['std_link_id'] = traffic_df['std_link_id']

    return traffic_df


if __name__ == "__main__":
    print(f"sys.argv = {sys.argv}")
    if len(sys.argv) != 4:
        print("Insufficient arguments.")
        sys.exit(1)
    # preparation.py 파일을 직접 실행 시 _model_name, _model_version, _base_day의
    # arguments가 정상적으로 전달받았는지 간단히 체크하기 위함임.

    _model_name = sys.argv[1]
    _model_version = sys.argv[2]
    _base_day = sys.argv[3]

    print(f"_model_name = {_model_name}")
    print(f"_model_version = {_model_version}")
    print(f"_base_day = {_base_day} !@#")

    preparation = Preparation(model_name=_model_name,
                              model_version=_model_version,
                              base_day=_base_day)
    preparation.preprocessing()