import Dashboard from "views/Dashboard.jsx";
import TableList from "views/TableList.jsx";
import Maps from "views/Maps.jsx";
import Chatbot from "views/Chatbot";
import RegisterBoard from "views/RegisterBoard"
import Boards from "views/Boards"

const dashboardRoutes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "nc-icon nc-chart-pie-35",
    component: Dashboard,
    layout: "/admin"
  },
  {
    path: "/table",
    name: "road info list",
    icon: "nc-icon nc-notes",
    component: TableList,
    layout: "/admin"
  },
  {
    path: "/maps",
    name: "Maps",
    icon: "nc-icon nc-pin-3",
    component: Maps,
    layout: "/admin"
  },
  {
    path: "/chat-bot",
    name: "chatbot",
    icon: "nc-icon nc-android",
    component: Chatbot,
    layout: "/admin"
  },
  {
    path: "/register-board",
    name: "register board",
    icon: "nc-icon nc-paper-2",
    component: RegisterBoard,
    layout: "/admin"
  },
  {
    path: "/boards",
    name: "boards",
    icon: "nc-icon nc-notes",
    component: Boards,
    layout: "/admin"
  },
  
];

export default dashboardRoutes;
