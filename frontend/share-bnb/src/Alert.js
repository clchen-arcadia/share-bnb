/**
 * This component renders an alert for forms.
 *
 * Props: err (string)
 * State: none
 *
 * SignUpForm, LoginForm -> Alert
 *
 */
function Alert({ err }) {
  console.log(err, "err in alert");
  return (
    <div class="alert alert-danger mt-3" role="alert">
      {`${err}`.replace('instance.', '')}
    </div>
  );
}

export default Alert;