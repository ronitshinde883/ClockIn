import { BrowserRouter, Routes, Route } from "react-router-dom";
import React from "react";

import AttendanceQR from "./AttendanceQr.jsx";
import ScanAttendance from "./ScanAttendance.jsx";

export function App() {
  const session = {
    id: 12,
    token: "1ee5f6e5-4e96-4860-8a8f-9c16786f0c6b",
    expires_at: "2026-09-09T00:16:19.456955Z",
  };

  const qrToken = `http://192.168.1.3:5173/attendance/scan/${session.token}`;

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <AttendanceQR 
              qrtoken={qrToken} 
              session={session} 
            />
          }
        />

        {/* Student scans QR and reaches this route */}
        <Route 
          path="/attendance/scan/:token" 
          element={<ScanAttendance />} 
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
