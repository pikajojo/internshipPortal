import {useState, useContext, useEffect} from "react";
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
    const [showMessageForm, setShowMessageForm] = useState(false);
    const toggleMessageForm = () => {
        setShowMessageForm(!showMessageForm);
    };
    const handleAccept = () => {
        axios.post("/api/companies/accept", { student_id: props.email})
            .then(res => {
            console.log('Candidate accepted: ', res.data);
            })
            .catch(err => {
            console.error("Error accepting: ", err);
            });
    };

    const handleReject = () => {
        axios.post("/api/companies/reject", { student_id: props.email})
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
            <button onClick={handleAccept}>Accept</button>
            <button onClick={handleReject}>Reject</button>
            <button onClick={handleDownload}>Download CV</button>
            <button onClick={toggleMessageForm}>
                {showMessageForm ? 'Hide Message Form' : 'Send Message'}
            </button>
            {showMessageForm && <MessageForm recipient={props.email} />}
        </div>
    );
}

function MessageForm({ recipient }) {
    const [message, setMessage] = useState("");

    const handleMessageChange = (e) => {
        setMessage(e.target.value);
    };

    const handleMessageSend = () => {
        axios.post("/api/messages/send", { recipient, message })
            .then((res) => {
                if (res.status >= 200 && res.status < 300) {
                    window.alert('Message sent!');
                } else {
                    window.alert('Failed to send message.');
                }
            });
    };

    return (
        <div>
            <textarea value={message} onChange={handleMessageChange} placeholder="Write your message here..." />
            <button onClick={handleMessageSend}>Send Message</button>
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
    return <div>loading...</div>;
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

function AcceptedCard(props) {
    const [showMessageForm, setShowMessageForm] = useState(false);
    const toggleMessageForm = () => {
        setShowMessageForm(!showMessageForm);
    };
    const handleCease = () => {
        axios.post("/api/companies/cease", { student_id: props.email})
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
            <button onClick={toggleMessageForm}>
                {showMessageForm ? 'Hide Message Form' : 'Send Message'}
            </button>
            {showMessageForm && <MessageForm recipient={props.email} />}
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