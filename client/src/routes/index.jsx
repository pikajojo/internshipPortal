import {Link} from "react-router-dom";
import * as React from "react";

export default function Index() {
    return (
        <div id="index-page">
            <p>Welcome, stranger!</p>
            <p>Please register or login, before you can do anything meaningful.</p>
             <nav>
          <li><Link to="/register">Register</Link></li>
          <li> <Link to="/login">Login</Link></li>
        </nav>
        </div>
    );
}