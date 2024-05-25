import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../login.css';
//import { handleLogin } from './root.jsx'; // 假设 handleLogin 在 auth.js 文件中定义

import { AuthContext } from '../auth';
import axios from "axios"; // 导入你的 AuthContext


function Login() {

    const auth = React.useContext(AuthContext);
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState({
    email: '',
    password: '',
    user_type:'',
  });

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value
    });
  };

 const handleSubmit = async (e) => {
    e.preventDefault(); // 阻止表单默认提交行为
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials) // 确保 credentials 在作用域内
        });
        console.log('Response status:', response.status);
        console.log('Response status text:', response.statusText);

        const res = await response.json();

        if (res.status === 'success') {
            // navigate('/students', {replace: true});
            console.log(res.data);
            auth.login(res.data, () => {
                if (res.data.user_type === 'students'){

                    navigate('/students', {replace: true});
                }
                 if (res.data.user_type === 'companies'){

                    navigate('/companies', {replace: true});
                }
                  if (res.data.user_type === 'instructors'){

                    navigate('/instructors', {replace: true});
                }
              // navigate(res.data.user_type, {replace: true});
        })
        }else {
            // 可以在这里处理登录失败的逻辑，例如显示错误消息
            console.error('Login failed:', res.message);
        }
    } catch (error) {
        // 处理网络错误或者其他错误
        console.error('Login error:', error);
    }
};
//   function handleLogin(res) {
//         axios.post("/api/login",res)
//             .then((res) => {
//                 auth.login(res.data, () => {
//                     navigate(res.data.user_type, {replace: true});
//                 })
//             });
//     };


          return (
              // <div>
              //     <form onSubmit={handleSubmit}>
              //         <h2>Login</h2>
              //         <div>
              //             <label>Email</label>
              //             <input
              //                 type="email"
              //                 name="email"
              //                 value={credentials.email}
              //                 onChange={handleChange}
              //                 required
              //             />
              //         </div>
              //         <div>
              //             <label>Password</label>
              //             <input
              //                 type="password"
              //                 name="password"
              //                 value={credentials.password}
              //                 onChange={handleChange}
              //                 required
              //             />
              //         </div>
              //         <div>
              //             <label>Role</label>
              //             <input
              //                 type="text"
              //                 name="user_type"
              //                 value={credentials.user_type}
              //                 onChange={handleChange}
              //                 required
              //             />
              //         </div>
              //         <button type = 'submit'>Login</button>
              //     </form>
              // </div>
              <div className="form-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2 className="form-title">Login</h2>
        <div className="input-group">
          <label htmlFor="email" className="input-label">Email</label>
          <input
            type="email"
            name="email"
            id="email"
            value={credentials.email}
            onChange={handleChange}
            className="input-field"
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="password" className="input-label">Password</label>
          <input
            type="password"
            name="password"
            id="password"
            value={credentials.password}
            onChange={handleChange}
            className="input-field"
            required
          />
        </div>
        <div className="input-group">
          <label htmlFor="user_type" className="input-label">Role</label>
          <input
            type="text"
            name="user_type"
            id="user_type"
            value={credentials.user_type}
            onChange={handleChange}
            className="input-field"
            required
          />
        </div>
        <button type="submit" className="form-button">Login</button>
      </form>
    </div>
          );
  };

export default Login;
