FROM python:3.9-slim
LABEL maintainer="mlops.study@gmail.com"

ARG USER_HOME=/home/mlops
ARG PREPARATION_SOURCE_PATH=data_preparation
# MODEL_SOURCE_PATH라는 변수를 정의하고 기본값으로 model을 사용한다.
# ineligible_loan_model 패키지 하위에 존재하는 model 패키지를 지정하기 위해서 사용된다.
ARG MODEL_SOURCE_PATH=model
ARG MODEL_OUTPUT_PATH=model_output
ARG REQUIREMENTS_PATH=docker

RUN groupadd --gid 1000 mlops \
    && useradd --uid 1000 --gid mlops --shell /bin/bash --create-home mlops


# 데이터 전처리 코드를 실행하는데 필요한 파일을 복사
COPY --chown=mlops:mlops ${PREPARATION_SOURCE_PATH}/preparation.py \
    ${USER_HOME}/data_preparation/

# prediction.py 추가
# 호스트 시스템의 prediction.py 파일을 컨테이너 내의 model 디렉터리로 복사한다.
# 해당 파일을 사용하는 계정은 mlops로 복사할 때 파이르이 소유자와 그룹을 mlops로 파일 소유권을 변경하지 않으면,
# 파이릉 사용할 권한이 없어 오류가 발생한다.

COPY --chown=mlops:mlops ${MODEL_SOURCE_PATH}/prediction.py \
    ${USER_HOME}/model/

COPY --chown=mlops:mlops ${MODEL_OUTPUT_PATH}/ \
    ${USER_HOME}/model_output/
COPY --chown=mlops:mlops ${REQUIREMENTS_PATH}/requirements.txt \
    ${USER_HOME}/

USER mlops

# Python 라이브러리를 설치
RUN mkdir -p ${USER_HOME}/mlops_data_store \
   && pip install --no-cache-dir \
          -r ${USER_HOME}/requirements.txt

WORKDIR ${USER_HOME}