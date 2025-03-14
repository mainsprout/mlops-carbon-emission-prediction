/** 1. 새로운 traffic 데이터 생성 */

/** 기존 데이터 삭제 */
DELETE FROM temp.traffic_model_features
WHERE creat_de = '{{ params.base_day }}';

INSERT INTO temp.traffic_model_features (creat_de, creat_hm, std_link_id, vol, pasng_spd)
SELECT '{{ params.base_day }}' AS creat_de,
       CASE WHEN RAND() < 0.5 THEN '1100'
            WHEN RAND() < 0.5 THEN '1320'
            ELSE '1335' END AS creat_hm,
       CASE WHEN RAND() < 0.5 THEN '2510590500'
            ELSE '2510590400' END AS std_link_id,
       CASE WHEN RAND() < 0.5 THEN 10
            ELSE 5 END AS vol,
       ROUND(RAND() * 100, 2) AS pasng_spd
FROM some_table
WHERE conditions
LIMIT 10;

/** 2. 필수 조건을 충족하는 데이터 생성 */

DELETE FROM temp.traffic_data_conditions
WHERE creat_de = '{{ params.base_day }}';

INSERT INTO temp.traffic_data_conditions (creat_de, creat_hm, std_link_id, vol, pasng_spd)
SELECT '{{ params.base_day }}' AS creat_de,
       '1100' AS creat_hm,
       '2510590500' AS std_link_id,
       10 AS vol,
       31.50 AS pasng_spd
UNION ALL
SELECT '{{ params.base_day }}' AS creat_de,
       '1320' AS creat_hm,
       '2510590400' AS std_link_id,
       5 AS vol,
       61.76 AS pasng_spd
UNION ALL
SELECT '{{ params.base_day }}' AS creat_de,
       '1325' AS creat_hm,
       '2510590400' AS std_link_id,
       5 AS vol,
       31.11 AS pasng_spd
UNION ALL
SELECT '{{ params.base_day }}' AS creat_de,
       '1335' AS creat_hm,
       '2510590400' AS std_link_id,
       5 AS vol,
       104.00 AS pasng_spd;
