import React, {useEffect, useState } from "react";
import ChartistGraph from "react-chartist";

import {
  Card,
  Container,
  Row,
  Col,
} from "react-bootstrap";

import { fetchPredictedData } from "../api/predict";


function Dashboard(props) {

  const [barData, setBarData] = useState({ labels: [], series: [[]] }); 
  const [pieData, setPieData] = useState({ labels: [], series: [] });

  const getColorForIndex = (index) => {
    const colors = [
      "#ff6384", "#36a2eb", "#cc65fe", "#ffce56", "#4bc0c0",
      "#9966ff", "#ff9f40", "#e8c3b9", "#c45850", "#8e5ea2",
    ];
    return colors[index % colors.length];
  };



  useEffect(() => {

    const initData = async () => {
      const creat_de = props.datetime.slice(0, 8); // YYYYMMDD
      const creat_hm = props.datetime.slice(8);   // HHmm
      const pasng_spd = props.speed;

      try {
        // 1. 중복 제거 (coordinates.sctn_nm 기준)
        const uniqueLocationInfos = props.locationInfos.reduce((acc, curr) => {
          const isDuplicate = acc.some(
            (item) => item.coordinates.sctn_nm === curr.coordinates.sctn_nm
          );
          return isDuplicate ? acc : [...acc, curr];
        }, []);

        console.log("Unique Location Infos:", uniqueLocationInfos);

        // 2. fetchPredictedData 호출 및 predict 값 가져오기
        const result = await Promise.all(
          uniqueLocationInfos.map(async (locationInfo) => {
            const std_link_id = locationInfo.coordinates.lid_link_i;
            const predict = await fetchPredictedData({
              creat_de,
              creat_hm,
              std_link_id,
              pasng_spd,
            });
            return {
              ...locationInfo,
              predict: predict.predict, // fetchPredictedData 결과 추가
            };
          })
        );

        // 3. 전체 predict 합 계산
        const totalPredict = result.reduce((sum, info) => sum + info.predict, 0);

        // 4. Bar Chart용 데이터 생성
        const newBarLabels = result.map((info) => info.coordinates.sctn_nm);
        const newBarSeries = result.map((info) => info.predict);

        const newBarData = {
          labels: newBarLabels,
          series: [newBarSeries], // Chartist의 Bar 차트는 series가 배열 배열 형태여야 함
        };

        // 5. Pie Chart용 데이터 생성 (백분율 기반)
        const newPieLabels = result.map(
          (info) =>
            `${info.coordinates.sctn_nm} (${(
              (info.predict / totalPredict) *
              100
            ).toFixed(2)}%)`
        );
        const newPieSeries = result.map((info) =>
          ((info.predict / totalPredict) * 100).toFixed(2)
        );

        const newPieData = {
          labels: newPieLabels,
          series: newPieSeries,
        };

        // 6. 상태 업데이트
        setBarData(newBarData);
        setPieData(newPieData);

        console.log("Bar Data:", barData);
        console.log("Pie Data:", pieData);

      } catch (error) {
        console.error("Error fetching predicted data:", error);
      }
    };

    if (props.datetime && props.locationInfos && props.locationInfos.length > 0) {
      initData();
    }
  }, [props.datetime, props.locationInfos, props.speed]);



  return (
    <>
      <Container fluid>
        <h2>각 구간 예상 탄소 배출량</h2>
        <Row>
          <Col md="6">
            <Card>
              
              <Card.Body>
                <div className="ct-chart" id="chartActivity" style={{ overflowX: "auto", height: "56vh" }}>
                  <ChartistGraph
                    data={barData}
                    type="Bar"
                    options={{
                      seriesBarDistance: 5, // 막대 간의 간격 설정
                      axisX: {
                        showGrid: false,
                      },
                      height: "50vh",
                      width: "100vw",
                    }}
                    responsiveOptions={[
                      [
                        "screen and (max-width: 640px)",
                        {
                          seriesBarDistance: 5,
                          axisX: {
                            labelInterpolationFnc: function (value) {
                              return value[0];
                            },
                          },
                        },
                      ],
                    ]}
                  />
                </div>

                {/* CSS 스타일로 막대 두께 설정 */}
                <style>
                  {`
                    #chartActivity .ct-bar {
                      stroke-width: 30px; /* 막대의 두께 설정 */
                    }
                  `}
                </style>
              </Card.Body>
            </Card>
          </Col>

          <Col md="6">
            <Card>
              <Card.Header>
                <Card.Title as="h4"></Card.Title>
                <p className="card-category"></p>
              </Card.Header>
              <Card.Body>
                <div
                  className="ct-chart ct-perfect-fourth"
                  id="chartPreferences"
                  style={{ width: "100%", height: "40vh", margin: "auto" }}
                >
                  <ChartistGraph
                    data={pieData}
                    type="Pie"
                    style={{height:"100%"}}
                    options={{
                      labelOffset: 50,  // 숫자를 가장자리로 이동
                      labelInterpolationFnc: function (value, index) {
                        // 숫자만 표시
                        return pieData.series[index] + "%";
                      },
                      chartPadding: 0,
                    }}
                  />
                </div>
                <div
                  className="legend"
                  style={{
                    maxHeight: "150px", // 최대 높이 설정
                    overflowY: "auto", // 수직 스크롤 추가
                    paddingRight: "10px", // 스크롤바와 텍스트 간격
                  }}
                >
                  {pieData.labels.map((label, index) => (
                    <div
                      key={index}
                      style={{
                        display: "flex",
                        alignItems: "center",
                        marginBottom: "5px",
                      }}
                    >
                      <span
                        style={{
                          display: "inline-block",
                          width: "20px",
                          height: "20px",
                          backgroundColor: getColorForIndex(index), // 색상 매핑 함수
                          marginRight: "10px",
                        }}
                      ></span>
                      <span>{label}</span>
                    </div>
                  ))}
                </div>

                <style>
                  {`
                    /* Dynamic Color Styles */
                    #chartPreferences .ct-series-a .ct-slice-pie { fill: #ff6384; }
                    #chartPreferences .ct-series-b .ct-slice-pie { fill: #36a2eb; }
                    #chartPreferences .ct-series-c .ct-slice-pie { fill: #cc65fe; }
                    #chartPreferences .ct-series-d .ct-slice-pie { fill: #ffce56; }
                    #chartPreferences .ct-series-e .ct-slice-pie { fill: #4bc0c0; }
                    #chartPreferences .ct-series-f .ct-slice-pie { fill: #9966ff; }
                    #chartPreferences .ct-series-g .ct-slice-pie { fill: #ff9f40; }
                    #chartPreferences .ct-series-h .ct-slice-pie { fill: #e8c3b9; }
                    #chartPreferences .ct-series-i .ct-slice-pie { fill: #c45850; }
                    #chartPreferences .ct-series-j .ct-slice-pie { fill: #8e5ea2; }
                    #chartPreferences .ct-series-k .ct-slice-pie { fill: #3cba9f; }
                    #chartPreferences .ct-series-l .ct-slice-pie { fill: #e8c3b9; }
                    #chartPreferences .ct-series-m .ct-slice-pie { fill: #c45850; }
                    #chartPreferences .ct-series-n .ct-slice-pie { fill: #ff6384; }
                    #chartPreferences .ct-series-o .ct-slice-pie { fill: #36a2eb; }
                    #chartPreferences .ct-series-p .ct-slice-pie { fill: #cc65fe; }
                    #chartPreferences .ct-series-q .ct-slice-pie { fill: #ffce56; }
                    #chartPreferences .ct-series-r .ct-slice-pie { fill: #4bc0c0; }
                  `}
                </style>
              </Card.Body>
            </Card>
          </Col>

        </Row>
      </Container>
    </>
  );
}

export default Dashboard;
