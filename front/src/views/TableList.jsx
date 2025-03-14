import React from "react";
// react-bootstrap components
import {
  Badge,
  Button,
  Card,
  Navbar,
  Nav,
  Table,
  Container,
  Row,
  Col,
} from "react-bootstrap";

function TableList(props) {
  console.log(props.locationInfos);
  return (
    <>
      <Container fluid>
        <Row>
          <Col md="12">
            <Card className="strpied-tabled-with-hover">
              <Card.Header>
                <Card.Title as="h4">원주 도로 정보</Card.Title>
                <p className="card-category">원주 지역의 도로 정보입니다.</p>
              </Card.Header>
              <Card.Body
                className="table-full-width table-responsive px-0"
                style={{ maxHeight: "75vh", overflowY: "auto" }}
              >
                <Table
                  className="table-hover table-striped"
                  style={{ position: "relative", borderCollapse: "separate" }}
                >
                  <thead
                    style={{
                      position: "sticky",
                      top: -15,
                      backgroundColor: "#f8f9fa", // 헤더 배경색 (필요 시 변경 가능)
                      zIndex: 1,
                    }}
                  >
                    <tr>
                      <th className="border-0">도로 구간 ID</th>
                      <th className="border-0">시작점 ID</th>
                      <th className="border-0">종료점 ID</th>
                      <th className="border-0">도로 경사</th>
                      <th className="border-0">도로 유형</th>
                      <th className="border-0">도로 관할 코드</th>
                      <th className="border-0">차선 수</th>
                      <th className="border-0">도로 번호</th>
                      <th className="border-0">최고 속도 제한</th>
                      <th className="border-0">도로 구간 이름</th>
                      <th className="border-0">도로 길이</th>
                    </tr>
                  </thead>
                  <tbody>
                    {props.locationInfos &&
                      props.locationInfos.map((info, idx) => (
                        <tr key={idx}>
                          <td>{info.coordinates.lid_link_i}</td>
                          <td>{info.coordinates.begin_lid_}</td>
                          <td>{info.coordinates.end_lid_no}</td>
                          <td>{info.coordinates.road_grad}</td>
                          <td>{info.coordinates.road_ty}</td>
                          <td>{info.coordinates.cnro_code}</td>
                          <td>{info.coordinates.lane_co}</td>
                          <td>{info.coordinates.route_no}</td>
                          <td>{info.coordinates.top_lmtt_s}</td>
                          <td>{info.coordinates.sctn_nm}</td>
                          <td>{info.coordinates.lt}</td>
                        </tr>
                      ))}
                  </tbody>
                </Table>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default TableList;
