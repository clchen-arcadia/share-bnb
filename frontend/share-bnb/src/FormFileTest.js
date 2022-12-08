import { useState } from 'react';
import axios from 'axios';

const BASE_URL = 'http://localhost:5001';

function FormFileTest() {
  const [name, setName] = useState("");
  const [selectedFiles, setSelectedFiles] = useState([]);
  console.log("FormFileTest rendered with selectedFiles=", selectedFiles);

  /** Def inline function for submitting form,
   *  uploads file to backend server.
   */
  const submitForm = (e) => {
    e.preventDefault();
    const formData = new FormData();

    for (let file of selectedFiles) {
      formData.append('file', file);
    }

    axios({
      method: 'post',
      url: `${BASE_URL}/upload`,
      data: formData,
    })
      .then(response => console.log(response))
      .catch(errors => console.log(errors));
  };

  return (
    <form onSubmit={submitForm}>
      <label>File Name:</label>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(() => e.target.value)}
      />

      <label>{"Select File(s):"}</label>
      <input
        type="file"
        multiple
        onChange={(e) => setSelectedFiles(() => e.target.files)}
      />

      <button>Submit!</button>
    </form>
  );
}

export default FormFileTest;
