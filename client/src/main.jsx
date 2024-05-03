import React from 'react'
import ReactDOM from 'react-dom/client'
import {createBrowserRouter, RouterProvider, BrowserRouter} from "react-router-dom";
import './index.css'
import Root from "./routes/root.jsx";
import {AuthProvider} from "./auth.jsx";
// import 'bootstrap/dist/css/bootstrap.min.css';
// import ErrorPage from "./error-page.jsx";
// import Index from "./routes/index.jsx";
// import Root from "./routes/root.jsx";
//
// const router = createBrowserRouter([
//     {
//         path: "/",
//         element: <Root />,
//         errorElement: <ErrorPage />,
//         children: [
//             {
//                 errorElement: <ErrorPage />,
//                 children: [
//                     {
//                         index: true,
//                         element: <Index />
//                     },
//                     {
//                         path:"students/companies",
//
//                     },
//                     {
//                         path:"companies/:companyId",
//                     },
//                     {
//                         path:"instructors/:instructorId",
//                     }
//                 ]
//             }
//         ]
//     }
// ]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
      {/*<RouterProvider router={router} />*/}
    <BrowserRouter>
        <AuthProvider>
            <Root />
        </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
