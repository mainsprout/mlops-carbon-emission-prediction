create database if not exists temp;
drop table if exists temp.traffic_model_features;
create table temp.traffic_model_features as
    select
        a.creat_de,
        a.creat_hm,
        a.std_link_id,
        a.vol,
        a.pasng_spd
    from mlops_project.area a
    order by a.creat_de
    limit 2000000 offset 563843;
/* 563843 오프셋값 준 이유는 LLID로 시작하지 않는 std_link_id 값들 빼려고 한거임*/

delete from mlops_project.traffic_model_features;
INSERT INTO mlops_project.traffic_model_features
    (
     creat_de,
     creat_hm,
     std_link_id,
     vol,
     pasng_spd
    )
SELECT
    a.creat_de,
    a.creat_hm,
    a.std_link_id,
    a.vol,
    a.pasng_spd
FROM temp.traffic_model_features a;

