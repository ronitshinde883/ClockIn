import React, {useEffect, useState} from "react";
import {useParams} from "react-router-dom";
import axios from "axios"

function ScanAttendance () {
    const {token} = useParams();

    const [message, setMessage] = useState("Marking attendance...")
    const [error, setError] = useState("")

    useEffect(() => {
        const markAttendance = async () => {
            try {
                // const accessToken = localStorage.getItem("accessToken")
                const accessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg4OTExNzUxLCJpYXQiOjE3ODg5MTE0NTEsImp0aSI6IjBjYTE5ZjVjOGYwNTRlZmJhMTBjYTMxMzg5YmU3MDA5IiwidXNlcl9pZCI6IjUifQ.0ajNESxK3AIvoNQr7NpHqCwSi1bvJBPuNyJ0qCeOnx8"

                const response = await axios.post(
                    `http://192.168.1.3:8000/api/attendance/mark/${token}/`,
                    {},
                    {
                        headers: {
                            Authorization: `Bearer ${accessToken}`
                        }
                    }
                );

                setMessage(response.data.message)
            } catch(error) {
                console.error(error)

                setError(
                    error.response?.data?.detail || 
                    error.response?.data?.error ||
                    "Failed to mark attendance"
                )

                setMessage("")
            }
        }

        markAttendance();
    }, [token]);

    return (
        <div>
            {message && <h2>{message}</h2>}
            {error && <h2>{error}</h2>}
        </div>
    )
}

export default ScanAttendance;