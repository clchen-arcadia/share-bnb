import { React, useContext } from "react";
import { NavLink, Link } from "react-router-dom";
import userContext from "./userContext";

/**
 * Renders a Navigation component
 *
 * State: none
 * Props: handleLogout: logout callback function
 *
 * App -> Navigation
 *
 * consuming userContext: username
 */

function Navigation({ handleLogout }) {
    const { username } = useContext(userContext);
    const isLoggedIn = username !== undefined;
    // const isLoggedIn = true;

    return (
        <nav className="Navigation">
            <div className="Navigation-homepage-link">
                <Link to="/">ShareBnB</Link>
            </div>
            {
                isLoggedIn
                    ?
                    <div className="Navigation-data-links">
                        <NavLink to="/listings">Listings</NavLink>
                        <NavLink to="/profile">Profile</NavLink>
                        <NavLink to={`/messages/${username}`}>Messages</NavLink>
                        <NavLink to={`/listings/${username}`}>My Listings</NavLink>
                        <NavLink
                            to="/logout"
                            onClick={handleLogout}
                            className="Navigation-data-links-logout"
                        >
                            Logout {username}
                        </NavLink>
                    </div>
                    :
                    <div className="Navigation-data-links">
                        <NavLink to="/login">Login</NavLink>
                        <NavLink to="/signup">Signup</NavLink>
                    </div>
            }
        </nav>
    );
}

export default Navigation;
