import { useState, useContext, useEffect } from "react";
import { CustomLink } from "../custom.jsx";
import { Outlet, useLoaderData } from "react-router-dom";
import axios from "axios";
import { RequireAuth, AuthContext } from "../auth.jsx";
import MessageForm from "./MessageForm";

function ProfileCard(props) {
    return (
        <div>
            <h2>{props.name}</h2>
            <img className="avatar" src={props.logo} alt={props.name} />
        </div>
    );
}

function MessageCard(props) {
    return (
        <div>
            <h3>From: Student ID {props.studentId} </h3>
            <p>{props.message}</p>
        </div>
    );
}

function AcceptedCard(props) {
    const handleCease = () => {
        axios.post("/api/companies/cease", { student_id: props.email })
            .then(res => {
                console.log('Contract terminated: ', res.data);
            })
            .catch(err => {
                console.error("Error ceasing: ", err);
            });
    };

    return (
        <div>
            <h2>{props.name}</h2>
            <p>Email: {props.email}</p>
            <p>Institute: {props.major}</p>
            <button onClick={handleCease}>Cease</button>
            <MessageForm studentId={props.email} recipientType="student" />
        </div>
    );
}

export function CompanyAccepted() {
    const accepteds = useLoaderData();
    return (
        <RequireAuth requiredUserType={'companies'}>
            <div>
                {
                    accepteds.map((accepted) => (
                        <AcceptedCard key={accepted.google_id} {...accepted} />
                    ))
                }
            </div>
        </RequireAuth>
    );
}

export function CompanyLayout() {
    const auth = useContext(AuthContext);

    return (
        <RequireAuth requiredUserType={'companies'}>
            <div>
                <ProfileCard {...(auth.userInfo)} />
                <nav>
                    <ul>
                        <li>
                            <CustomLink to={"/companies"}>Pending</CustomLink>
                        </li>
                        <li>
                            <CustomLink to={"/companies/accepted"}>Accepted</CustomLink>
                        </li>
                        <li>
                            <CustomLink to={"/companies/messages"}>Messages</CustomLink>
                        </li>
                    </ul>
                </nav>
                <hr />
                <Outlet />
            </div>
        </RequireAuth>
    );
}

export function CompanyMessages() {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        axios.get("/api/companies/messages").then((res) => {
            console.log("Received messages:", res.data);
            setMessages(res.data);
        });
    }, []);

    return (
        <RequireAuth requiredUserType={'companies'}>
            <div>
                {messages.length > 0 ? (
                    messages.map((message) => (
                        <MessageCard key={message._id} studentId={message.student_id} message={message.message} />
                    ))
                ) : (
                    <p>No messages available.</p>
                )}
            </div>
        </RequireAuth>
    );
}

export async function pendingLoader() {
    const res = await axios.get("/api/companies/pending");
    return res.data;
}

function PendingCard(props) {
    const handleAccept = () => {
        axios.post("/api/companies/accept", { student_id: props.email })
            .then(res => {
                console.log('Candidate accepted: ', res.data);
            })
            .catch(err => {
                console.error("Error accepting: ", err);
            });
    };

    const handleReject = () => {
        axios.post("/api/companies/reject", { student_id: props.email })
            .then(res => {
                console.log('Candidate rejected: ', res.data);
            })
            .catch(err => {
                console.error("Error rejecting: ", err);
            });
    };

    const handleDownload = () => {
        axios.post('/api/companies/cv', { file_id: props.cv })
            .then((res) => {
                const blob = new Blob([res.data], { type: 'application/pdf' });
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', `${props.name}_cv.pdf`);
                document.body.appendChild(link);
                link.click();
                link.parentNode.removeChild(link);
                window.URL.revokeObjectURL(url);
            })
            .catch((error) => {
                console.error('Error downloading CV:', error);
            });
    };

    return (
        <div>
            <h2>{props.name}</h2>
            <p>Email: {props.email}</p>
            <p>Institute: {props.institute}</p>
            <button onClick={handleAccept}>Accept</button>
            <button onClick={handleReject}>Reject</button>
            <button onClick={handleDownload}>Download CV</button>
            <MessageForm recipientId={props.email} recipientType="student" />
        </div>
    );
}

export function CompanyPending() {
    const [pendings, setPendings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await axios.get('/api/companies/pending');
                setPendings(res.data);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <RequireAuth requiredUserType={'companies'}>
            <div>
                {
                    pendings.map((pending) => (
                        <PendingCard key={pending.email} {...pending} />
                    ))
                }
            </div>
        </RequireAuth>
    );
}

export async function acceptedLoader() {
    const res = await axios.get("/api/companies/accepted");
    return res.data;
}