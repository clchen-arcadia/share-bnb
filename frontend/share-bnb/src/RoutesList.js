import { Route, Routes, Navigate } from "react-router-dom";
import Homepage from "./Homepage.js";
import userContext from "./userContext.js";
import { useContext } from "react";
import MessageChatRoom from './MessageChatRoom';
import ProfileForm from './UserEditForm';
import ListingsPage from './ListingsPage';
import ListingNewForm from "./ListingNewForm.js";
import ListingEditForm from "./ListingEditForm";
import LoginForm from './UserLoginForm';
import SignupForm from './UserSignupForm';
import ListingDetailsPage from './ListingDetailsPage.js';

/**
 * Renders a RoutesList component.
 *
 * State: none
 * Props: handleLogin, handleSignup, handleProfileEdit
 *
 * App -> RoutesList
 *
 * Accessible routes determined by data in localstorage("token")
 *
 * userContext consumed: username
 */

function RoutesList({ handleLogin, handleSignup, handleProfileEdit }) {
    const { data } = useContext(userContext);
    const isLoggedIn = data?.username !== undefined;
    // const isLoggedIn = true;

    return (
        <div className="RoutesList">
            {isLoggedIn
                ?
                <Routes>
                    <Route path="/messages/:curr_user/:to_user" element={<MessageChatRoom />} />

                    <Route path="/profile" element={<ProfileForm onSubmit={handleProfileEdit} />} />

                    <Route path="/listings" element={<ListingsPage />} />
                    <Route path="/listings/new" element={<ListingNewForm />} />
                    <Route path="/listings/:id" element={<ListingDetailsPage />} />
                    <Route path="/listings/:id/edit" element={<ListingEditForm />} />

                    <Route path="/" element={<Homepage />} />
                    <Route path="*" element={<Navigate to="/" />} />
                </Routes>

                :
                <Routes>
                    <Route path="/listings" element={<ListingsPage />} />
                    <Route path="/login" element={<LoginForm onSubmit={handleLogin} />} />
                    <Route path="/signup" element={<SignupForm onSubmit={handleSignup} />} />
                    <Route path="/" element={<Homepage />} />
                    <Route path="*" element={<Navigate to="/" />} />
                </Routes>
            }
        </div>
    );
}

export default RoutesList;
