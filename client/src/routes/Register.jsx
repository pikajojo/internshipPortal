import React, { useState } from 'react';
import axios from "axios";
import '../register.css';

function Register({handleRegister}) {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    user_type:'',
  });

  const [error, setError] = useState('');

  // const handleChange = (e) => {
  //   setFormData({
  //     ...formData,
  //     [e.target.name]: e.target.value
  //   });
  // };
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

 const handleSubmit = async (event) => {
    event.preventDefault();
    const userData = {
      username: event.target.username.value,
      email: event.target.email.value,
      password: event.target.password.value,
      user_type: event.target.user_type.value,
    };
    handleRegister(userData, setError);  // 使用传入的 handleRegister 函数
  };

  return (
    //   <div>
    // <form onSubmit={handleSubmit}>
    //   <h2>Register</h2>
    //   <div>
    //     <label>Username</label>
    //     <input
    //       type="text"
    //       name="username"
    //       value={formData.username}
    //       onChange={handleChange}
    //       required
    //     />
    //   </div>
    //   <div>
    //     <label>Email</label>
    //     <input
    //       type="email"
    //       name="email"
    //       value={formData.email}
    //       onChange={handleChange}
    //       required
    //     />
    //   </div>
    //   <div>
    //     <label>Password</label>
    //     <input
    //       type="password"
    //       name="password"
    //       value={formData.password}
    //       onChange={handleChange}
    //       required
    //     />
    //   </div>
    //      <div>
    //     <label>Role</label>
    //     {/*<select name="user_type" value={formData.user_type} onChange={handleChange}>*/}
    //     {/*        <option value="students">Student</option>*/}
    //     {/*        <option value="companys">Company</option>*/}
    //     {/*        <option value="instructors">Instructor</option>*/}
    //     {/*    </select>*/}
    //          <input
    //       type="text"
    //       name="user_type"
    //       value={formData.user_type}
    //       onChange={handleChange}
    //       required
    //     />
    //   </div>
    //   <button type="submit">Register</button>
    // </form>
    //   {error && <p className="error">{error}</p>}
    // </div>
       <div className="form-container">
      <h1 className="title">Internship Portal</h1>
      <h2 className="subtitle">Register</h2>
      <form className="register-form" onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="username">Username</label>
          <input  required type="text" id="username" name="username" value={formData.username} onChange={handleChange} />
        </div>
        <div className="input-group">
          <label htmlFor="email">Email</label>
          <input type="email" id="email" name="email" />
        </div>
        <div className="input-group">
          <label htmlFor="password">Password</label>
          <input  required type="password" id="password" name="password" value={formData.password} onChange={handleChange} />
        </div>
        <div className="input-group">
          <label htmlFor="role">Role</label>
          <input type="text" id="user_type" name="user_type" value={formData.user_type} onChange={handleChange}/>
        </div>
        <button type="submit" className="register-button">Register</button>
      </form>
      <p className="login-link">
        Already have an account? <a href="/login">Login here</a>
      </p>
    </div>
  );
}

export default Register;
