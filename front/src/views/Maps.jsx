import React, { useEffect, useRef, useState } from "react";
import styled from "styled-components";
import Papa from 'papaparse';


// 예시: 폴리곤용 API (기존 코드)
import { fetchPredictedData } from "../api/predict";

// ----- (1) 스타일 정의
const MapContainer = styled.div`
  width: 100%;
  height: 80vh;
  display: flex;
  flex-direction: column;
`;

const MapDiv = styled.div`
  width: 100%;
  height: 100%;
`;

// ----- (2) 컴포넌트 구현
const Maps = (props) => {
  const mapRef = useRef(null);
  const [busStops, setBusStops] = useState([]); // CSV 데이터를 저장할 상태

// CSV 파일 로드 및 파싱
  const loadCSVData = async () => {
    try {
      // 로컬 CSV 파일 경로
      const response = await fetch("/wonju_bus_info.csv");
      const csvText = await response.text();

      // CSV 파일 파싱
      Papa.parse(csvText, {
        header: true, // 첫 번째 줄을 헤더로 사용
        skipEmptyLines: true, // 빈 줄 무시
        complete: (result) => {
          setBusStops(result.data); // 파싱된 데이터를 상태에 저장
        },
        error: (error) => {
          console.error("CSV 파일 파싱 오류:", error);
        },
      });
    } catch (error) {
      console.error("CSV 파일 로드 오류:", error);
    }
  };


  // 지도 초기화 함수
  const initTmap = async () => {
    if (!window.Tmapv3) {
      console.error("Tmap API가 로드되지 않았습니다.");
      return;
    }

    // (2-1) 지도 생성
    const map = new window.Tmapv3.Map("Tmap", {
      center: new window.Tmapv3.LatLng(37.38000000000000, 127.95000000000000),
      zoom: 10.5,
    });
    mapRef.current = map;

    // (2-2) 폴리곤(또는 폴리라인) 그리기 (기존 로직 유지)
    if (props.datetime) {
      for (const locationInfo of props.locationInfos) {
        try {
          const creat_de = props.datetime.slice(0, 8); // YYYYMMDD
          const creat_hm = props.datetime.slice(8);    // HHmm
          const std_link_id = locationInfo.std_link_id;
          const pasng_spd = props.speed;

          // API 호출
          const res = await fetchPredictedData({ creat_de, creat_hm, std_link_id, pasng_spd });
          const predict = res.predict;

          // 혼잡도에 따른 색상 설정
          let color;
          if (predict > 55) color = "#FF0000";   // 붉은색
          else if (predict > 50) color = "#FFA500"; // 주황색
          else color = "#00FF00";               // 초록색

          // 좌표 배열 -> Tmapv3.LatLng 배열로 변환
          const polygonPath = locationInfo.coordinates.Coordinates.map((coord) => {
            return new window.Tmapv3.LatLng(coord[1], coord[0]);
          });

          // 폴리곤(또는 폴리라인) 생성
          new window.Tmapv3.Polygon({
            paths: polygonPath,
            strokeWeight: 4,      // 선 두께
            strokeColor: color,   // 선 색상
            strokeOpacity: 0.8,   // 선 투명도
            fillColor: "none",    // 내부 채우기 색상
            fillOpacity: 0,       // 내부 투명도
            map: map,
          });
        } catch (e) {
          console.error("Error rendering location:", locationInfo, e);
        }
      }
    }

    // (2-3) CSV에서 읽어온 버스정류장 위치를 지도에 마커로 표시
    // if (props.busStops && Array.isArray(props.busStops)) {
    //   props.busStops.forEach((busStop) => {
    //     // CSV 특성상 문자열이므로 number로 변환
    //     const lat = parseFloat(busStop["위도"]);
    //     const lng = parseFloat(busStop["경도"]);

    //     // 위도, 경도가 숫자로 변환되었다면 마커 생성
    //     if (!isNaN(lat) && !isNaN(lng)) {
    //       new window.Tmapv3.Marker({
    //         position: new window.Tmapv3.LatLng(lat, lng),
    //         map: map,
    //         // title 옵션에 정류장명 혹은 정류장번호 등 표시 가능
    //         title: busStop["버스정류장명"] || "버스정류장",
    //       });
    //     }
    //   });
    // }


  };

  useEffect(() => {
    loadCSVData();
    console.log(busStops)
  }, [])

  // (3) useEffect에서 지도 초기화 및 해제 처리
  useEffect(() => {

    if (props.locationInfos && props.locationInfos.length > 0) {
      initTmap();
    }
    
    return () => {
      // 언마운트 시(또는 datetime 등의 props가 바뀔 때) 기존 지도를 제거
      if (mapRef.current) {
        mapRef.current.destroy();
        mapRef.current = null;
      }
    };

  }, [props.datetime, props.locationInfos, props.speed, busStops]);

  // (4) 렌더링
  return (
    <MapContainer className="MapContainer">
      <MapDiv id="Tmap" className="MapDiv" />
    </MapContainer>
  );
};

export default Maps;
