import { useState } from "react";
import axios from "axios";

function MessageForm({ recipientId, recipientType }) {
    const [message, setMessage] = useState('');
    const [error, setError] = useState(null);

    const handleSendMessage = () => {
        const endpoint = recipientType === 'student' ? '/api/companies/message' : '/api/students/message';
        const payload = recipientType === 'student'
            ? { student_id: recipientId, message }
            : { company_id: recipientId, message };

        axios.post(endpoint, payload)
            .then(res => {
                if (res.status >= 200 && res.status < 300) {
                    window.alert('Message sent!');
                    setMessage('');
                    setError(null);
                } else {
                    // window.alert('Message sending failed! Please try again later.');
                    setError('Message sending failed! Please try again later.');
                }
            })
            .catch(err => {
                console.error("Error sending message: ", err);
                setError(err.response?.data?.error || 'Message sending failed! Please try again later.');
            });
    };

    return (
        <div>
            <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Write your message here..."
            ></textarea>
            <button onClick={handleSendMessage}>Send Message</button>
            {error && <p style={{ color: 'red' }}>{error}</p>}
        </div>
    );
}

export default MessageForm;
