import { QRCodeSVG } from "qrcode.react";

function AttendanceQR({ session }) {

    return (
        <div>
            <h2>Scan to mark attendance</h2>

            <QRCodeSVG
                value={session.token}
                size={300}
            />

            <p>Expires at: {session.expires_at}</p>
        </div>
    );
}

export default AttendanceQR;