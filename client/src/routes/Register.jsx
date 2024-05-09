import React, { useState } from 'react';
import axios from "axios";

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
      <div>
    <form onSubmit={handleSubmit}>
      <h2>Register</h2>
      <div>
        <label>Username</label>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label>Email</label>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          required
        />
      </div>
      <div>
        <label>Password</label>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />
      </div>
         <div>
        <label>Role</label>
        {/*<select name="user_type" value={formData.user_type} onChange={handleChange}>*/}
        {/*        <option value="students">Student</option>*/}
        {/*        <option value="companys">Company</option>*/}
        {/*        <option value="instructors">Instructor</option>*/}
        {/*    </select>*/}
             <input
          type="text"
          name="user_type"
          value={formData.user_type}
          onChange={handleChange}
          required
        />
      </div>
      <button type="submit">Register</button>
    </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Register;
