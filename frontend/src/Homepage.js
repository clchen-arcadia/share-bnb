import { useContext } from 'react';
import userContext from './userContext';

function Homepage() {
  const context = useContext(userContext);
  const firstName = context?.data?.firstName;
  const isLoggedIn = firstName !== undefined;

  return (
    <div className="Homepage">
      <h1>
        Welcome to ShareBnB!
      </h1>
      {
        isLoggedIn
          ? <p>Welcome back {firstName}!</p>
          : <p>
            Hint: Sign up with a username/password/email (you can use 'something@email.com') or sign in with:
            <br />username: u1
            <br />password: password
          </p>
      }
    </div>
  );
}

export default Homepage;
