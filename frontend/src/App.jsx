import { useState } from "react";
import { QRCodeSVG } from "qrcode.react";

import AttendanceQR from "./AttendanceQr.jsx";

function App() {

  const session = {
    id: 12,
    token: "550e8400-e29b-41d4-a716-446655440000",
    expires_at: "2026-09-07T19:40:00Z"
  }

  return (
    <div>
      <AttendanceQR session={session}></AttendanceQR>
    </div>
  )
}

export default App;
