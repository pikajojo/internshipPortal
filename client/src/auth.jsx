import * as React from "react";
import {Navigate, useLocation} from "react-router-dom";

export const AuthContext = React.createContext({
    userInfo: null,
    setUserInfo: null,
    login: null,
    logout: null,
});

export function AuthProvider({ children }) {
    const [userInfo, setUserInfo] = React.useState(null);
    const login = (newUserInfo, callback) => {
        setUserInfo(newUserInfo);
        callback();
    }
    const logout = (callback) => {
        setUserInfo(null);
        callback();
    }
    const value = {userInfo, setUserInfo, login, logout};
    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// export function useAuth() {
//     return React.useContext(AuthContext);
// }

export function RequireAuth({children, requiredUserType}) {
    const auth = React.useContext(AuthContext);
    const location = useLocation();
    if(!auth.userInfo || auth.userInfo.user_type != requiredUserType) {
        return <Navigate to={"/"} state={{ from: location }} replace={true} />;
    }
    return children;
}