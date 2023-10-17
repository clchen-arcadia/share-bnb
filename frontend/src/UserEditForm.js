import { useContext } from 'react';
import userContext from './userContext';

function UserEditForm() {
  const context = useContext(userContext);
  const userInfo = context.data

  return (
    <div className="UserEditForm">
      <h1>
        User Information
      </h1>
      <p>
        First Name: {userInfo.firstName}
        <br />Last Name: {userInfo.lastName}
        <br />Email: {userInfo.email}
        <br />Is Admin: {String(userInfo.isAdmin)}
        <br />Is A Host: {String(userInfo.isHost)}
      </p>

    </div>
  )
}

export default UserEditForm;
