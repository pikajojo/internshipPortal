import {useState, useContext} from "react";
import {CustomLink} from "../custom.jsx";
import {Outlet, useLoaderData} from "react-router-dom";
import axios from "axios";
import {RequireAuth, AuthContext} from "../auth.jsx";

function ProfileCard(props) {
    return (
        <div>
            <h2>{props.name}</h2>
            <img className="avatar" src={props.logo} alt={props.name} />
        </div>
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
                    </ul>
                </nav>
                <hr />
                <Outlet />
            </div>
        </RequireAuth>
    )
}

export async function pendingLoader() {
    const res = await axios.get("/api/companies/pending");
    return res.data
}

function PendingCard(props) {
    const handleAccept = () => {
        axios.post("/api/companies/accept", { student_id: props.google_id})
            .then(res => {
            console.log('Candidate accepted: ', res.data);
            })
            .catch(err => {
            console.error("Error accepting: ", err);
            });
    };

    const handleReject = () => {
        axios.post("/api/companies/reject", { student_id: props.google_id})
            .then(res => {
                console.log('Candidate rejected: ', res.data);
            })
            .catch(err => {
                console.error("Error rejecting: ", err);
            });
    };

    const handleDownload = () => {
        axios.post("/api/companies/cv", {file_id: props.cv})
            .then(res => {
            const blob = new Blob([res.data], { type: 'application/pdf' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', props.name + '_cv.pdf');
            document.body.appendChild(link);
            link.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(link);
            })
            .catch(error => {
            console.error('Error downloading CV:', error);
            });
    }

    return (
        <div>
            <h2> {props.name} </h2>
            <p>Email: {props.email}</p>
            <p>Institute: {props.institute}</p>
            <button onClick={handleAccept}>Accept</button>
            <button onClick={handleReject}>Reject</button>
            <button onClick={handleDownload}>Download CV</button>
        </div>
    );
}

export function CompanyPending() {
    const pendings = useLoaderData();
    return (
        <RequireAuth requiredUserType={'companies'}>
            <div>
            {
                    pendings.map((pending) => (
                        <PendingCard key={pending.google_id} {...pending} />
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

function AcceptedCard(props) {
    const handleCease = () => {
        axios.post("/api/companies/cease", { student_id: props.google_id})
            .then(res => {
                console.log('Contract terminated: ', res.data);
            })
            .catch(err => {
                console.error("Error ceasing: ", err);
            });
    };

    return (
        <div>
            <h2> {props.name} </h2>
            <p>Email: {props.email}</p>
            <p>Institute: {props.institute}</p>
            <button onClick={handleCease}>Cease</button>
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