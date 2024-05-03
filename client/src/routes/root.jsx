import {
    Outlet, Routes, Route, Link, useMatch, useResolvedPath, useNavigate, useLocation, Navigate
} from "react-router-dom";
import * as React from "react";
import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import { Navbar, Nav, Button } from 'react-bootstrap';
import {AuthProvider, RequireAuth, AuthContext} from "../auth.jsx";
import Index from "./index.jsx";
import {NotFoundPage} from "../error-page.jsx";
import {
    StudentLayout, StudentCompanies, StudentInstructors, StudentEdit,
    // companiesLoader as studentCompaniesLoader,
    // instructorsLoader as studentInstructorsLoader
} from "./students.jsx";
import {
    CompanyLayout, CompanyPending, CompanyAccepted,
    // pendingLoader as companyPendingLoader,
    // acceptedLoader as companyAcceptedLoader
} from "./companies.jsx";

const GOOGLE_OAUTH_CLIENT_ID = "298770111102-pjqiii259fb57ue60428vfdbo0s2i0ko.apps.googleusercontent.com";

export default function Root() {
     const auth = React.useContext(AuthContext);
     // const location = useLocation();
     const navigate = useNavigate();

    React.useEffect(() => {
        axios.get("/api/whoami").then((res) => {
            if (res.data.google_id) {
                auth.setUserInfo(res.data);
            }
        });
    }, []);

    const handleLogin = (res) => {
        axios.post("/api/login", {token: res.credential})
            .then((res) => {
                auth.login(res.data, () => {
                    navigate(res.data.user_type, {replace: true});
                })
        });
    };

    const handleLogout = () => {
        axios.post("/api/logout");
        auth.logout(() => {
            navigate("/", {replace: true});
        });
    }

    return (
        <GoogleOAuthProvider clientId={GOOGLE_OAUTH_CLIENT_ID}>
            {/*<AuthProvider>*/}
                <div>
                    <h1>Internship Portal</h1>
                    {auth.userInfo ? (
                        <Button variant="primary"
                                onClick={handleLogout}>
                            Logout
                        </Button>
                    ) : (
                        <GoogleLogin
                            onSuccess={handleLogin}
                            onError={() => {
                                console.log('Login Failed');
                            }}
                        />
                    )}
                    <Routes>
                        <Route index element={<Index />} />
                        <Route path={"students"} element={<StudentLayout/>}>
                            <Route
                                index
                                element={<StudentCompanies/>}
                                // loader={studentCompaniesLoader}
                            />
                            <Route
                                path={"instructors"}
                                element={<StudentInstructors/>}
                                // loader={studentInstructorsLoader}
                            />
                            <Route path={"edit"} element={<StudentEdit/>}/>
                            <Route path={"*"} element={<NotFoundPage/>}/>
                        </Route>
                        <Route path={"companies"} element={<CompanyLayout/>}>
                            <Route
                                index
                                element={<CompanyPending/>}
                                // loader={companyPendingLoader}
                            />
                            <Route
                                path={"accepted"}
                                element={<CompanyAccepted/>}
                                // loader={companyAcceptedLoader}
                            />
                            <Route path={"*"} element={<NotFoundPage/>}/>
                        </Route>
                        {/*<Route path={"instructors"} element={<InstructorLayout/>}>*/}
                        {/*    <Route index element={<InstructorStudents/>}/>*/}
                        {/*    <Route path={"*"} element={<Ops/>}/>*/}
                        {/*</Route>*/}
                    </Routes>
                </div>
            {/*</AuthProvider>*/}
        </GoogleOAuthProvider>
    );
}