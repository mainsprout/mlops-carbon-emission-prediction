import React, { useState, useRef, useEffect } from "react";
import { useLocation, Route, Switch } from "react-router-dom";

import AdminNavbar from "components/Navbars/AdminNavbar";
import Sidebar from "components/Sidebar/Sidebar";
import routes from "routes.js";
import sidebarImage from "assets/img/sidebar-3.jpg";

import { fetchLocationInfoByStdlinkid } from "../api/location";

function Admin() {
  const [image, setImage] = useState(sidebarImage);
  const [color, setColor] = useState("black");
  const [hasImage, setHasImage] = useState(true);
  const [locationInfos, setLocationInfos] = useState([]);
  const [datetime, setDatetime] = useState("");
  const [speed, setSpeed] = useState(0.0);
  const [polygonData, setPolygonData] = useState([]); // 폴리곤 데이터 상태
  const [boards, setBoards] = useState([]);
  const [selectedBoard, setSelectedBoard] = useState(null);

  const location = useLocation();
  const mainPanel = useRef(null);

  const std_link_id_list = [
    "LLID100061", "LLID100397", "LLID100458", "LLID100469", "LLID100126",
    "LLID100418", "LLID100470", "LLID100413", "LLID100415", "LLID100223",
    "LLID100465", "LLID100222", "LLID100466", "LLID100395", "LLID100468",
    "LLID100467", "LLID100256", "LLID100330", "LLID100293", "LLID100361",
    "LLID100382", "LLID100365", "LLID100399", "LLID100401", "LLID100271",
    "LLID100406", "LLID100277", "LLID100440", "LLID100439",
    "LLID100449", "LLID100381", "LLID100101", "LLID100167", "LLID100447",
    "LLID100392", "LLID100199", "LLID100227", "LLID100283", "LLID100289",
    "LLID100298", "LLID100443", "LLID100394", "LLID100335", "LLID100374",
    "LLID100376", "LLID100389", "LLID100402", "LLID100409", "LLID100462",
    "LLID100446", "LLID100451", "LLID100292", "LLID100452", "LLID100454",
    "LLID100455", "LLID100445", "LLID100460", "LLID100344", "LLID100453",
    "LLID100349", "LLID100333", "LLID100461", "LLID100218", "LLID100360",
    "LLID100404", "LLID100407", "LLID100434", "LLID100464",
    "LLID100463", "LLID100431", "LLID100393", "LLID100252", "LLID100181",
    "LLID100432", "LLID100144", "LLID100441"
  ];

  const handleBoardClick = (board) => {
    setSelectedBoard(board);
  };

  const closeDetail = () => {
    setSelectedBoard(null);
  };

  const addBoard = (newBoard) => {
    setBoards([...boards, newBoard]);
  };
  

  const fetchData = async () => {
    try {
      let new_locationInfos = [];

      const promises = std_link_id_list.map(async (info) => {
        const data = await fetchLocationInfoByStdlinkid(info);
        return data;
      });
  
      new_locationInfos = await Promise.all(promises);

        new_locationInfos.sort((a, b) => {
          return a.coordinates.sctn_nm.localeCompare(b.coordinates.sctn_nm);
        });
  
      setLocationInfos(new_locationInfos);
    } catch (e) {
      console.error(e);
    }
  };

  const getRoutes = (routes) => {
    return routes.map((prop, key) => {
      if (prop.layout === "/admin") {
        if(prop.name === "Maps" || prop.name === "road info list" || prop.name === "Dashboard") {
          return (
            <Route
              path={prop.layout + prop.path}
              render={(props) => <prop.component {...props} locationInfos={locationInfos} datetime={datetime} speed={speed}/>}
              key={key}
            />
          )
        }
        else if (prop.name === "register board") {
          return (
            <Route
              path={prop.layout + prop.path}
              render={(props) => <prop.component {...props} addBoard={addBoard} />}
              key={key}
            />
          )
        }
        else if (prop.name === "boards") {
          return (
            <Route
              path={prop.layout + prop.path}
              render={(props) => <prop.component {...props} boards={boards} setSelectedBoard={handleBoardClick} />}
              key={key}
            />
          )
        }
        else {
          return (
            <Route
              path={prop.layout + prop.path}
              render={(props) => <prop.component {...props} />}
              key={key}
            />
          );
        }
      } 
      else {
        return null;
      }
    });
  };

  useEffect(() => {
    fetchData();
  }, [])

  return (
    <div className="wrapper">
      <Sidebar color={color} image={hasImage ? image : ""} routes={routes} />
      <div className="main-panel" ref={mainPanel}>
        <AdminNavbar updateDatetime={setDatetime} setSpeed={setSpeed}/>
        <div className="content">
          <Switch>{getRoutes(routes)}</Switch>
        </div>
      </div>
    </div>
  );
}

export default Admin;
