import os
import sys
import joblib
import pandas as pd


feature_store_url = os.getenv('FEATURE_STORE_URL', "")
model_output_home = os.getenv('MODEL_OUTPUT_HOME', "")
mlops_data_store = os.getenv('MLOPS_DATA_STORE', "")

class Preparation:
  def __init__(self,
              model_name: str,
              base_day: str):
      self._model_name = model_name
      self._base_day = base_day
      self._data_preparation_path = f"{mlops_data_store}/data_preparation" \
                                    f"/{self._model_name}/ct/{self._base_day}"
      self._encoder_path = f"{self._data_preparation_path}/encoders"
      self._makedir()


  def preprocessing(self):
      traffic_df = self._get_features_extracted()
      traffic_df = self._set_random_sample(traffic_df)
      # self._fill_na_to_default(traffic_df)
      # traffic_df = self._transform_to_one_hot_encoding(traffic_df)
      traffic_df = self._transform_to_label_encoding(traffic_df)
      numeric_features = ['pasng_spd']
      self._transform_to_standard_scale(traffic_df, numeric_features)
      self._transform_to_min_max_scale(traffic_df, numeric_features)
      self._save_encoded_features(traffic_df)


  def _makedir(self):
      if not os.path.isdir(self._encoder_path):
          os.makedirs(self._encoder_path)


  def _save_encoded_features(self, traffic_df):
    print("save traffic_df = ", traffic_df)
    """
    피처 데이터 저장
    """
    feature_file_name = f"{self._model_name}.csv"
    traffic_df.to_csv(f"{self._data_preparation_path}"
                      f"/{feature_file_name}", index=False)


  def _transform_to_min_max_scale(self, traffic_df, numeric_features):
    from sklearn.preprocessing import MinMaxScaler

    min_max_scalers = {}
    for numeric_feature in numeric_features:
      min_max_scaler = MinMaxScaler()
      min_max_scalers[numeric_feature] = min_max_scaler.fit(
          traffic_df[[numeric_feature]])

    # min_max_scalers 저장
    joblib.dump(min_max_scalers,
                f'{self._encoder_path}/min_max_scalers.joblib')

    print(f"numeric_features 정규화")
    for numeric_feature in numeric_features:
      min_max_scaler = min_max_scalers[numeric_feature]
      print(f"numeric_feature = {numeric_feature}")

      traffic_df[numeric_feature] = min_max_scaler.transform(
          traffic_df[[numeric_feature]])


  def _transform_to_standard_scale(self, traffic_df, numeric_features):
    from sklearn.preprocessing import StandardScaler
    standard_scalers = {}
    for numeric_feature in numeric_features:
      standard_scaler = StandardScaler()
      standard_scalers[numeric_feature] = standard_scaler.fit(
          traffic_df[[numeric_feature]])
    joblib.dump(standard_scalers,
                f'{self._encoder_path}/standard_scalers.joblib')

    print(f"numeric_features 표준화")
    for numeric_feature in numeric_features:
      standard_scaler = standard_scalers[numeric_feature]
      print(f"numeric_feature = {numeric_feature}")

      traffic_df[numeric_feature] = standard_scaler.transform(
          traffic_df[[numeric_feature]])
    return traffic_df


  def _transform_to_label_encoding(self, traffic_df):
    from sklearn.preprocessing import LabelEncoder

    # 라벨 인코딩
    label_encoder = LabelEncoder()
    traffic_df['std_link_id'] = label_encoder.fit_transform(traffic_df['std_link_id'])
    # label_encoders 저장
    joblib.dump(label_encoder,
                f'{self._encoder_path}/label_encoders.joblib')
    print(traffic_df[['std_link_id']].head())

    return traffic_df


  @staticmethod
  def _fill_na_to_default(traffic_df):
    traffic_df['std_link_id'].fillna(method='ffill', inplace=True)
    traffic_df['vol'].fillna(traffic_df['vol'].mean(), inplace=True)
    traffic_df['pasng_spd'].fillna(traffic_df['pasng_spd'].mean(), inplace=True)
    traffic_df['datetime'].fillna(method='ffill', inplace=True)

  @staticmethod
  def _set_random_sample(traffic_df):
    random_state = 100
    traffic_df = traffic_df.sample(frac=1,
                                   random_state=random_state).reset_index(drop=True)
    return traffic_df


  def _get_features_extracted(self):
    from sqlalchemy import create_engine, text
    engine = create_engine(feature_store_url)
    ## 데이터 추출(01_data_extract.sql) 결과를 조회한다.
    sql = f"""
        select *
          from mlops_project.traffic_model_features
    """

    with engine.connect() as conn:
      traffic_df = pd.read_sql(text(sql), con=conn)

    if traffic_df.empty:
      raise ValueError("traffic df is empty!")

    traffic_df['datetime'] = pd.to_datetime(
    traffic_df['creat_de'] + ' ' + traffic_df['creat_hm'])
    traffic_df['datetime'] = traffic_df['datetime'].dt.strftime('%Y%m%d%H%M')
    traffic_df['datetime'] = traffic_df['datetime'].astype('int64')
    traffic_df.drop(columns=['creat_de', 'creat_hm'], inplace=True)
    traffic_df['std_link_id'] = traffic_df['std_link_id'].astype('category')

    return traffic_df


if __name__ == "__main__":
  print(f"sys.argv = {sys.argv}")
  if len(sys.argv) != 3:
    print("Insufficient arguments")
    sys.exit(1)

  from support.date_values import DateValues

  _model_name = sys.argv[1]
  _base_day = sys.argv[2]
  _base_ym = DateValues().get_before_one_day(_base_day)

  print(f"_model_name = {_model_name}")
  print(f"_base_day = {_base_day}")
  print(f"_base_ym = {_base_ym}")

  preparation = Preparation(model_name=_model_name,
                            base_day=_base_ym)
  preparation.preprocessing()