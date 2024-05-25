import {useResolvedPath, useMatch, Link} from "react-router-dom";

export function CustomLink({children, to, ...props}) {
    const resolvedPath = useResolvedPath(to);
    const match = useMatch(resolvedPath.pathname, true);
    return (
        <div>
            <Link style={{textDecoration: match ? "underline" : "none"}} to={to} {...props}>
                {children}
            </Link>
        </div>
    );
}