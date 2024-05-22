import {
    Outlet, Routes, Route, Link, useNavigate
} from "react-router-dom";
import * as React from "react";
import axios from 'axios';
import { Navbar, Nav, Button } from 'react-bootstrap';
import { AuthProvider, RequireAuth, AuthContext } from "../auth.jsx";
import Index from "./index.jsx";
import { NotFoundPage } from "../error-page.jsx";
import {
    StudentLayout, StudentCompanies, StudentInstructors, StudentEdit,
} from "./students.jsx";
import {
    CompanyLayout, CompanyPending, CompanyAccepted
} from "./companies.jsx";
import Login from './Login.jsx';
import Register from './Register.jsx';
import InboxCard from './InboxCard.jsx';

export default function Root() {
    const auth = React.useContext(AuthContext);
    const navigate = useNavigate();

    React.useEffect(() => {
        axios.get("/api/whoami").then((res) => {
            if (res.data.email) {
                auth.setUserInfo(res.data);
            }
        });
    }, []);

    const handleRegister = (userData, setError) => {
        axios.post("/api/register", userData)
            .then((res) => {
                navigate('/login', { replace: true });
            })
            .catch((error) => {
                if (error.response) {
                    setError(error.response.data.message);
                } else {
                    setError('Register failed, please try again later.');
                }
            });
    };

    const handleLogout = () => {
        axios.post("/api/logout");
        auth.logout(() => {
            navigate("/", { replace: true });
        });
    };

    return (
        <AuthProvider>
            <div>
                {auth.userInfo !== null ? (
                    <Button variant="primary" onClick={handleLogout}>
                        Logout
                    </Button>
                ) : (
                    <>
                        <Routes>
                            <Route index element={<Index />} />
                            <Route path={"Register"} element={<Register handleRegister={handleRegister} />} />
                            <Route path={"Login"} element={<Login />} />
                            <Route path={"students"} element={<StudentLayout />}>
                                <Route path={"companies"} element={<StudentCompanies />} />
                                <Route path={"instructors"} element={<StudentInstructors />} />
                                <Route path={"edit"} element={<StudentEdit />} />
                                <Route path={"inbox"} element={<InboxCard />} />  {/* Add this line */}
                                <Route path={"*"} element={<NotFoundPage />} />
                            </Route>
                            <Route path={"companies"} element={<CompanyLayout />}>
                                <Route index element={<CompanyPending />} />
                                <Route path={"accepted"} element={<CompanyAccepted />} />
                                <Route path={"*"} element={<NotFoundPage />} />
                            </Route>
                        </Routes>
                    </>
                )}
            </div>
        </AuthProvider>
    );
}
