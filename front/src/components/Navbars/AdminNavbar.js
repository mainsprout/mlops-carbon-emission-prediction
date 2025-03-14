import React, { useState } from "react";
import { useLocation, useHistory } from "react-router-dom"; // useHistory 추가
import { Navbar, Container, Nav } from "react-bootstrap";
import "react-dates/initialize";
import "react-dates/lib/css/_datepicker.css";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import TextField from "@mui/material/TextField";
import { format } from "date-fns";

function Header(props) {
  const location = useLocation();
  const history = useHistory(); // useHistory 사용
  const [dateTime, setDateTime] = useState(new Date());
  const [doubleValue, setDoubleValue] = useState(""); // double 값 상태 관리

  const handleDoubleChange = (e) => {
    const value = e.target.value;
    if (!isNaN(value) && value !== "") {
      setDoubleValue(value);
    } else if (value === "") {
      setDoubleValue("");
    }
  };

  return (
    <Navbar bg="light" expand="lg">
      <Container fluid>
        <Navbar.Collapse id="basic-navbar-nav">
          <Nav className="nav mr-auto" navbar>
            <Nav.Item>
              <div
                style={{ display: "flex", alignItems: "center", padding: "0 10px" }}
              >
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                  <DateTimePicker
                    label="Date & Time"
                    value={dateTime}
                    onChange={(newValue) => setDateTime(newValue)}
                    renderInput={(params) => <TextField {...params} />}
                  />
                </LocalizationProvider>
              </div>
            </Nav.Item>

            <Nav.Item>
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  padding: "0 10px",
                  maxWidth: "200px",
                }}
              >
                <TextField
                  label="Enter Double"
                  type="number"
                  variant="outlined"
                  size="middle"
                  value={doubleValue}
                  onChange={handleDoubleChange}
                  inputProps={{
                    step: "0.01", // 소수점 단위
                  }}
                  fullWidth
                />
              </div>
            </Nav.Item>

            <Nav.Item>
              <Nav.Link
                className="m-0"
                href="#pablo"
                onClick={(e) => {
                  e.preventDefault();
                  props.setSpeed(doubleValue)
                  props.updateDatetime(format(dateTime, "yyyyMMddHHmm"));
                }}
              >
                <i className="nc-icon nc-zoom-split"></i>
                <span className="d-lg-block"> Search</span>
              </Nav.Link>
            </Nav.Item>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default Header;
