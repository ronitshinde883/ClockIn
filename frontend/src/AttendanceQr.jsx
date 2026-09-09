import { QRCodeSVG } from "qrcode.react";

function AttendanceQR({ qrtoken, session }) {

    return (
        <div>
            <h2>Scan to mark attendance</h2>

            <QRCodeSVG
                value={qrtoken}
                size={300}
            />

            <p>Expires at: {session.expires_at}</p>
        </div>
    );
}

export default AttendanceQR;