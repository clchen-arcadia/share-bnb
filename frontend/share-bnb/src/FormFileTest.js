import { useState } from 'react';
import axios from 'axios';

const BASE_URL = 'http://localhost:5001';

function FormFileTest() {
  const [name, setName] = useState("");
  const [selectedFile, setSelectedFile] = useState("");

  /** Def inline function for submitting form,
   *  uploads file to backend server.
   */
  const submitForm = (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("name", name);
    formData.append("file", selectedFile);

    console.log("formData=", formData);
    const dataSubmit = {
      name,
      selectedFile
    };
    console.log("dataSubmit=", dataSubmit);
    for(let data of formData.values) {
      console.log("data is", data);
    }

    axios
      .post(`${BASE_URL}/upload`, dataSubmit)
      .then((res) => {
        alert("File Upload success");
      })
      .catch((err) => alert("File Upload Error"));
  };


  return (
    <form onSubmit={submitForm}>
      <label>File Name:</label>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />

      <label>Select File:</label>
      <input
        type="file"
        onChange={(e) => setSelectedFile(e.target.files[0])}
      />

      <button>Submit!</button>
    </form>
  );
}

export default FormFileTest;
