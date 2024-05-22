import React from "react";

function InboxCard({ messages }) {
    const newMessageCount = messages.filter(msg => !msg.read).length;

    return (
        <div>
            <h2>Inbox</h2>
            {newMessageCount > 0 && <p>{newMessageCount} new messages</p>}
            <ul>
                {messages.map((msg) => (
                    <li key={msg._id}>
                        <p><strong>From:</strong> {msg.sender}</p>
                        <p><strong>Message:</strong> {msg.message}</p>
                        <p><strong>Timestamp:</strong> {new Date(msg.timestamp).toLocaleString()}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default InboxCard;
