import {useState, useContext, useEffect} from "react";
import {CustomLink} from "../custom.jsx";
import {Outlet, useLoaderData} from "react-router-dom";
import axios from "axios";
import { AuthContext, RequireAuth } from "../auth.jsx";

function ProfileCard(props) {
    return (
        <div>
            <h2>{props.name}</h2>
            <img className="avatar" src={props.avatar} alt={props.name} />
            <ul>
                <li>Email: {props.email}</li>
                <li>Institute: {props.institute}</li>
            </ul>
        </div>
    );
}

function CompanyCard(props) {
    const [showDetail, setShowDetail] = useState(false);
    const [message, setMessage] = useState('');
    const toggleDetail = () => {
        setShowDetail(!showDetail)
    };

    const handleApply = () => {
        axios.post("/api/students/apply", {"company_id": props.email})
            .then((res) => {
                if(res.status >= 200 && res.status < 300) {
                    window.alert('Submitted!');
                } else {
                    window.alert('Application failed! Please try again later and ' +
                        'double-check that your resume has been uploaded correctly.');
                }
            })
    };

    const handleSendMessage = () => {
        axios.post("/api/students/message", {"company_id": props.email, "message": message})
            .then((res) => {
                if(res.status >= 200 && res.status < 300) {
                    window.alert('Message sent!');
                    setMessage('');
                } else {
                    window.alert('Message sending failed! Please try again later.');
                }
            })
    };

    return (
        <div>
            <h2>{props.name}</h2>
            <img className="avatar" src={props.logo} alt={props.name} />
            <ul>
                <li>Location: {props.location}</li>
                <li>Website: {props.website}</li>
                {
                    showDetail &&
                    <>
                        <li>Email: {props.email}</li>
                        <li>Tel: {props.phone}</li>
                        <li>Description: {props.description}</li>
                    </>
                }
            </ul>
            <button onClick={toggleDetail}>
                {showDetail ? 'Hide detail' : 'Show detail'}
            </button>
            <button onClick={handleApply} disabled={props.state !== 'none'}>
                {props.state === 'none' ? "Apply": props.state === 'accepted' ? "Accepted" : "Pending"}
            </button>
            <div>
                <textarea value={message} onChange={(e) => setMessage(e.target.value)} placeholder="Write your message here..."></textarea>
                <button onClick={handleSendMessage}>Send Message</button>
            </div>
        </div>
    );
}

function InstructorCard(props) {
    return (
        <div>
            <h2>{props.name}</h2>
            <img className="avatar" src={props.avatar} alt={props.name} />
            <ul>
                <li>Email: {props.email}</li>
                <li>Institute: {props.institute}</li>
            </ul>
        </div>
    );
}

export function StudentLayout() {
    const auth = useContext(AuthContext);
    return (
         <RequireAuth requiredUserType={'students'}>
            <div>
                <ProfileCard {...(auth.userInfo)} />
                <nav>
                    <ul>
                        <li>
                            <CustomLink to={"/students/companies"}>Companies</CustomLink>
                        </li>
                        <li>
                            <CustomLink to={"/students/instructors"}>Instructors</CustomLink>
                        </li>
                        <li>
                            <CustomLink to={"/students/edit"}>Edit</CustomLink>
                        </li>
                    </ul>
                </nav>
                <hr />
                <Outlet />
            </div>
         </RequireAuth>
    );
}

async function companiesLoader() {
    const res = await axios.get("/api/students/companies");
    return res.data;
}

export function StudentCompanies() {
    const [companies, setCompanies] = useState([]);
    useEffect(() => {
        companiesLoader().then((val) => setCompanies(val));
    }, []);

    return (
         <RequireAuth requiredUserType={'students'}>
               {companies && companies.length > 0 ? (
        <div>
          {companies.map((company) => (
            <CompanyCard key={company.email} {...company} />
          ))}
        </div>
      ) : (
        <p>No companies available.</p>
      )}
         </RequireAuth>
    );
}

async function instructorsLoader() {
    const res = await axios.get("/api/students/instructors");
    return res.data;
}

export function StudentInstructors() {
    const [instructors, setInstructors] = useState([]);
    useEffect(() => {
        instructorsLoader().then((val) => setInstructors(val));
    }, []);

    return (
         <RequireAuth requiredUserType={'students'}>
            instructors &&
                <div>
                    {
                        instructors.map((instructor) => (
                            <InstructorCard key={instructor.email} {...instructor} />
                        ))
                    }
                </div>

         </RequireAuth>
    );
}

export function StudentEdit() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [institute, setInstitute] = useState('');
    const [major, setMajor] = useState('');

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

      const handleInstituteChange = (event) => {
        setInstitute(event.target.value);
    };

    const handleMajorChange = (event) => {
        setMajor(event.target.value);
    };

    const handleUpload = () => {
        if (selectedFile && institute && major) {
            const formData = new FormData();
            formData.append('file', selectedFile);
            formData.append('institute', institute);
            formData.append('major', major);
            axios.post("/api/students/edit", formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then((res) => {
                window.alert('Information updated!');
                console.log(res);
            }).catch((err) => {
                window.alert("Something went wrong!");
                console.log(err);
            });
        }
    }

    return (
        // <RequireAuth requiredUserType={'students'}>
            <div>
                <h2> Upload CV / Proposal / CoverLetter </h2>
                <label>
                    Institute:
                    <input type='text' value ={institute} onChange={handleInstituteChange} />
                </label>
                <label>
                    Major:
                    <input type='text' value ={major} onChange={handleMajorChange} />
                </label>
                <label>
                    CV / Proposal / CoverLetter:
                    <input type='file' onChange={handleFileChange} accept={".pdf"}/>
                </label>
                <button onClick={handleUpload}>Upload</button>
            </div>
        // </RequireAuth>
    )
}
// export function StudentEdit() {
//     const [selectedFile, setSelectedFile] = useState(null);
//     const [institute, setInstitute] = useState('');
//     const [major, setMajor] = useState('');
//
//     const handleFileChange = (event) => {
//         setSelectedFile(event.target.files[0]);
//     };
//
//     const handleInstituteChange = (event) => {
//         setInstitute(event.target.value);
//     };
//
//     // const handleMajorChange = (event) => {
//     //     setMajor(event.target.value);
//     // };
//
//     const handleUpload = () => {
//         const formData = new FormData();
//         if (selectedFile) {
//             formData.append('file', selectedFile);
//         }
//         // formData.append('institute', institute);
//         // formData.append('major', major);
//
//         axios.post("/api/students/edit", formData, {
//             headers: {
//                 'Content-Type': 'multipart/form-data'
//             }
//         }).then((res) => {
//             window.alert('Details updated successfully!');
//             console.log(res);
//         }).catch((err) => {
//             window.alert("Something went wrong!");
//             console.log(err);
//         });
//     }

    // return (
    //     <div>
    //         <h2>Upload CV and Edit Details</h2>
    //         <div>
    //             <label>
    //                 Institute:
    //                 <input type='text' value={institute} onChange={handleInstituteChange} />
    //             </label>
    //         </div>
    //         <div>
    //             <label>
    //                 Major:
    //                 <input type='text' value={major} onChange={handleMajorChange} />
    //             </label>
    //         </div>
    //         <div>
    //             <label>
    //                 CV / Proposal / CoverLetter (PDF):
    //                 <input type='file' onChange={handleFileChange} accept={".pdf"} />
    //             </label>
    //         </div>
    //         <button onClick={handleUpload}>Upload</button>
    //     </div>
    // );}





