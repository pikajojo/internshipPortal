import React, { useState, useContext, useEffect } from "react";
import { CustomLink } from "../custom.jsx";
import { Outlet, useLoaderData } from "react-router-dom";
import axios from "axios";
import { RequireAuth, AuthContext } from "../auth.jsx";

function ProfileCard(props) {
    return (
        <div>
            <h2>{props.name}</h2>
            <img className="avatar" src={props.logo} alt={props.name} />
        </div>
    );
}

export function InstructorLayout() {
    const auth = useContext(AuthContext);
    return (
        <RequireAuth requiredUserType={'instructors'}>
            <div>
                <ProfileCard {...(auth.userInfo)} />
                <nav>
                    <ul>
                        <li>
                            <CustomLink to={"/instructors"}>To Review</CustomLink>
                        </li>
                        <li>
                            <CustomLink to={"/instructors/reviewed"}>Reviewed</CustomLink>
                        </li>
                    </ul>
                </nav>
                <hr />
                <Outlet />
            </div>
        </RequireAuth>
    );
}

export async function toReviewLoader() {
    const res = await axios.get("/api/instructors/toreview");
    return res.data;
}

function ToReviewCard(props) {
    const [showModal, setShowModal] = useState(false);
    const [message, setMessage] = useState("");

    const handleReview = () => {
        axios.post("/api/instructors/review", { student_id: props.email })
            .then(res => {
                console.log('Candidate reviewed: ', res.data);
                setShowModal(true);
            })
            .catch(err => {
                console.error("Error reviewing: ", err);
            });
    };

    const handleSendMessage = () => {
        axios.post('/api/instructors/message', { student_id: props.email, message: message })
            .then(res => {
                console.log('Message sent: ', res.data);
                setShowModal(false);
            })
            .catch(err => {
                console.error("Error sending message: ", err);
            });
    };

    const handleDownload = () => {
        axios.post('/api/companies/cv', { file_id: props.cv })
            .then((res) => {
                const blob = new Blob([res.data], { type: 'application/pdf' });
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', props.name + '_cv.pdf');
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
            <h2> {props.name} </h2>
            <p>Email: {props.email}</p>
            <p>Institute: {props.institute}</p>
            <button onClick={handleReview}>Review</button>
            {showModal && (
                <div className="modal">
                    <h2>Student Info</h2>
                    <p>Name: {props.name}</p>
                    <p>Email: {props.email}</p>
                    <p>Institute: {props.institute}</p>
                    <p>Course: {props.course}</p>
                    <textarea
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder="Write your message here"
                    />
                    <button onClick={handleSendMessage}>Send Message</button>
                    <button onClick={() => setShowModal(false)}>Close</button>
                </div>
            )}
            <button onClick={handleDownload}>Download CV</button>
        </div>
    );
}

export function InstructorToReview() {
    const [toReview, setToReview] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await axios.get('/api/instructors/toreview');
                setToReview(res.data);
            } catch (err) {
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return <div>loading...</div>;
    }

    if (error) {
        return <div>Error: {error.message}</div>;
    }
    return (
        <RequireAuth requiredUserType={'instructors'}>
            <div>
                {
                    toReview.map((student) => (
                        <ToReviewCard key={student.email} {...student} />
                    ))
                }
            </div>
        </RequireAuth>
    );
}

export async function reviewedLoader() {
    const res = await axios.get("/api/instructors/reviewed");
    return res.data;
}

function ReviewedCard(props) {
    const [showModal, setShowModal] = useState(false);
    const [message, setMessage] = useState("");

    const handleSendMessage = () => {
        axios.post('/api/instructors/message', { student_id: props.email, message: message })
            .then(res => {
                console.log('Message sent: ', res.data);
                setShowModal(false);
            })
            .catch(err => {
                console.error("Error sending message: ", err);
            });
    };

    return (
        <div>
            <h2>{props.name}</h2>
            <p>Email: {props.email}</p>
            <p>Institute: {props.institute}</p>
            <p>Course: {props.course}</p>
            <button onClick={() => setShowModal(true)}>Send Another Message</button>
            {showModal && (
                <div className="modal">
                    <h2>Send Message to {props.name}</h2>
                    <textarea
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        placeholder="Write your message here"
                    />
                    <button onClick={handleSendMessage}>Send Message</button>
                    <button onClick={() => setShowModal(false)}>Close</button>
                </div>
            )}
        </div>
    );
}

export function InstructorReviewed() {
    const revieweds = useLoaderData();
    return (
        <RequireAuth requiredUserType={'instructors'}>
            <div>
                {
                    revieweds.map((reviewed) => (
                        <ReviewedCard key={reviewed.google_id} {...reviewed} />
                    ))
                }
            </div>
        </RequireAuth>
    );
}


