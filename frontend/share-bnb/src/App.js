
import './App.css';
import { useState, useEffect } from 'react';
import useLocalStorage from "./useLocalStorage";
import userContext from "./userContext.js";
import RoutesList from './RoutesList';
import { BrowserRouter } from 'react-router-dom';
import Navigation from "./Navigation.js";
import ShareBnbApi from './Api.js';
import decode from "jwt-decode";

// localStorage.setItem("token", token);

// localStorage.removeItem("token");

// static token = localStorage.getItem("token");


export const TOKEN_STORAGE_ID = "sharebnb-token";

function App() {


  const [currentUser, setCurrentUser] = useState({
    data: null,
    infoLoaded: false
  });
  const [token, setToken] = useLocalStorage(TOKEN_STORAGE_ID);

  console.debug(
    "App",
    "currentUser=",
    currentUser,
    "token=",
    token
  );

  // Load user info from API. Until a user is logged in and they have a token,
  // this should not run. It only needs to re-run when a user logs out, so
  // the value of the token is a dependency for this effect.

  useEffect(
    function loadUserInfo() {
      console.debug("App useEffect loadUserInfo", "token=", token);

      async function getCurrentUser() {
        if (token) {
          try {
            let { username } = decode(token);
            // put the token on the Api class so it can use it to call the API.
            ShareBnbApi.token = token;
            let currentUser = await ShareBnbApi.getCurrentUser(username);
            console.log(currentUser, "<-----------------currentUser");
            setCurrentUser({
              infoLoaded: true,
              data: currentUser
            });
          } catch (err) {
            console.error("App loadUserInfo: problem loading", err);
            setCurrentUser({
              infoLoaded: true,
              data: null
            });
          }
        } else {
          setCurrentUser({
            infoLoaded: true,
            data: null
          });
        }
      }
      getCurrentUser();
    },
    [token]
  );


  /** Handles site-wide login.
   *
   * Logs in a user
   *
   * Make sure you await this function to see if any error happens.
   */
  async function handleLogin(loginData) {
    let token = await ShareBnbApi.login(loginData);
    setToken(token);
  }

  /**
   * Function called when Signup form is submitted.
   * Calls static method on JoblyApi.
   * Sets token state.
   */

  async function handleSignup(formData) {
    const token = await ShareBnbApi.registerNewUser(formData);
    setToken(token);
  }

  /**
   *  Function called when Logout button is clicked.
   *  Function sets the token state to the null.
   */

  function handleLogout() {
    localStorage.removeItem("token");
    setToken(() => null);
  }

  if (!currentUser.infoLoaded) {
    return <h1>Loading!</h1>;
  }



  return (
    <userContext.Provider value={currentUser}>
      <div className="App">
        <BrowserRouter>
          <Navigation
            handleLogout={handleLogout}
          />

          <RoutesList
            handleLogin={handleLogin}
            handleSignup={handleSignup}
          />
        </BrowserRouter>
      </div>
    </userContext.Provider>
  );
}

export default App;
