-- 임시 데이터베이스 temp가 존재하지 않으면 생성
create database if not exists temp;

-- 테이블이 존재할 경우 삭제 후 새로 생성
drop table if exists temp.traffic_model_features;

-- temp.traffic_model_features 테이블이 존재하지 않으면 생성
create table if not exists temp.traffic_model_features (
    creat_de	VARCHAR(25),
    creat_hm	VARCHAR(25),
    std_link_id	VARCHAR(25),
    vol	BIGINT(15),
    pasng_spd	DECIMAL(5,2)
);


insert into mlops_project.traffic_model_features
    (creat_de, creat_hm, std_link_id, vol, pasng_spd)
select creat_de, creat_hm, std_link_id, vol, pasng_spd
from temp.traffic_model_features;



drop table if exists mlops_project.traffic_model_result;
create table mlops_project.traffic_model_result
    (
    creat_de	VARCHAR(25),
    creat_hm	VARCHAR(25),
    std_link_id	VARCHAR(25),
    vol	BIGINT(15),
    pasng_spd	DECIMAL(5,2)
    );