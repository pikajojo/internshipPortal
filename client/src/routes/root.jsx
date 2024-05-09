import {
    Outlet, Routes, Route, Link, useMatch, useResolvedPath, useNavigate, useLocation, Navigate, BrowserRouter
} from "react-router-dom";
import * as React from "react";

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

import Login from './Login.jsx';   // 引入登录组件
import Register from './Register.jsx'; // 引入注册组件








// const GOOGLE_OAUTH_CLIENT_ID = "298770111102-pjqiii259fb57ue60428vfdbo0s2i0ko.apps.googleusercontent.com";

export default function Root() {
    const auth = React.useContext(AuthContext);
    // const location = useLocation();
    const navigate = useNavigate();

    React.useEffect(() => {
        axios.get("/api/whoami").then((res) => {
            if (res.data.email) {
                auth.setUserInfo(res.data);
            }
        });
    }, []);



    const handleRegister = (userData,  setError) => {
  axios.post("/api/register", userData)
    .then((res) => {
      navigate('/login', { replace: true });
    })
    .catch((error) => {
      // 处理错误，例如显示错误消息
      if (error.response){
          setError(error.response.data.message);
      }else{
          setError('Register failed, please try again later.')
      }
    });
};

    const handleLogout = () => {
        axios.post("/api/logout");
        auth.logout(() => {
            navigate("/", {replace: true});
        });
    }

        return (
             <AuthProvider>
        <div>

           {/*<h1>Internship Portal</h1>*/}
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

       </>
        )}
      </div>
                 </AuthProvider>

    );

}

