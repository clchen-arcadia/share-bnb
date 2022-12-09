import logo from './logo.svg';
import './App.css';
import FormFileTest from './FormFileTest';
import GetAndDisplayImage from './GetAndDisplayImages';

import { useState, useEffect } from 'react';
import userContext from "./userContext.js";
import './App.css';
import RoutesList from './RoutesList';
import { BrowserRouter } from 'react-router-dom';
import Navigation from "./Navigation.js";
import ShareBnbApi from './Api.js';
import jwt_decode from "jwt-decode";

// localStorage.setItem("token", token);

// localStorage.removeItem("token");

// static token = localStorage.getItem("token");




function App() {


  const [userInfo, setUserInfo] = useState({});
  const [token, setToken] = useState(localStorage.getItem("token"))

  console.log("userInfo>>>>>>>>>>>", userInfo);
  console.log("token>>>>>>>>>", token);
  /**
   * Every time the token state changes, function runs.
   * If token is not null, an API call will be made and userInfo
   * will be updated.
   * If the token is null, userInfo will be set to empty object.
   */
  useEffect(function handleChangeOfUser() {
    async function fetchUserInfo() {
      //console.log("useEffect invoked, token is", token);
      ShareBnbApi.token = token;
      if (token !== null) {
        localStorage.setItem("token", token);
        //console.log("there is a token, we got here");
        const tokenDecoded = jwt_decode(token);
        //console.log("TEST decoded token is>>>>", tokenDecoded);
        const { username } = tokenDecoded;

        try {
          const res = await ShareBnbApi.getUserInfo(username);
          setUserInfo(() => res.user);
        } catch (err) {
          handleLogout();
          //This happens only in odd circumstances where the server drops
          //in the moment after a successful login request
          window.alert("Login failed, please try again");
        }
      } else if (token === null) {
        localStorage.removeItem("token");
        setUserInfo({});
      }

      console.log("hallelujah, useEffect has been invoked");
    }

    fetchUserInfo();
  }, [token]);


  /**
   *  Function called when login form submitted.
   *  Call static methods on JoblyApi
   *  Sets token state.
   */

  async function handleLogin(formData) {
    const res = await ShareBnbApi.loginUser(formData);
    setToken(res.token);
  }

  /**
   * Function called when Signup form is submitted.
   * Calls static method on JoblyApi.
   * Sets token state.
   */

  async function handleSignup(formData) {
    const res = await ShareBnbApi.registerNewUser(formData);
    setToken(res.token);
  }

  /**
   *  Function called when ProfileForm data is submitted.
   *  Function calls JoblyApi static method to update user information.
   */

  async function handleProfileEdit({ firstName, lastName, email, username }) {
    const res = await ShareBnbApi.updateUserInfo(username, { firstName, lastName, email });
    //console.log("What is handleProfileEdit formData",formData, res);
    setUserInfo(userInfo => ({ ...userInfo, ...res.user }));
  }

  /**
   *  Function called when Logout button is clicked.
   *  Function sets the token state to the null.
   */

  function handleLogout() {
    localStorage.removeItem("token");
  }

  if (userInfo.username === undefined && token !== null) {
    return <h1>Loading!</h1>
  }



  return (
    <div className="App">
      <BrowserRouter>
          <Navigation
            handleLogout={handleLogout}
          />

          <RoutesList
            handleLogin={handleLogin}
            handleSignup={handleSignup}
            handleProfileEdit={handleProfileEdit}
          />
      </BrowserRouter>
    </div>
  );
}

export default App;
