import './Navigation.css';
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
    const { data } = useContext(userContext);
    const isLoggedIn = data?.username !== undefined;
    // const isLoggedIn = true;

    return (
        <nav className="Navigation d-flex justify-content-between">
            <div className="Navigation-homepage-link">
                <Link to="/" className="Link">ShareBnB</Link>
            </div>
            {
                isLoggedIn
                    ?
                    <div className="Navigation-data-links">
                            <NavLink to="/listings" className="Link">Listings</NavLink>
                            <NavLink to="/profile" className="Link">Profile</NavLink>
                            <NavLink to={`/messages/${data?.username}/any`} className="Link">Messages</NavLink>
                            <NavLink to={`/listings/user/${data?.username}`} className="Link">My Listings</NavLink>
                            <NavLink
                                to="/logout"
                                onClick={handleLogout}
                                className="Navigation-data-links-logout"
                            >
                                Logout {data?.username}
                            </NavLink>
                    </div>
                    :
                    <div className="Navigation-data-links">
                        <NavLink to="/login" className="Link">Login</NavLink>
                        <NavLink to="/signup" className="Link">Signup</NavLink>
                    </div>
            }
        </nav>
    );
}

export default Navigation;
