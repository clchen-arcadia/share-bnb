import { useState } from 'react';
import axios from 'axios';

const BASE_URL = 'http://localhost:5001';

function FormFileTest() {
  const [name, setName] = useState("");
  const [selectedFiles, setSelectedFiles] = useState([]);
  console.log(selectedFiles, "selected Files");
  /** Def inline function for submitting form,
   *  uploads file to backend server.
   */
  const submitForm = (e) => {
    e.preventDefault();
    const formData = new FormData();
    console.log(selectedFiles, "selected files!!!!!!!!!!!!!");

    Array.from(selectedFiles).forEach(file => {
      formData.append('file', file);
    });

    // for (let i = 0; i < selectedFiles.length; i++) {
    //   formData.append('file', selectedFiles[i]);
    // }

    formData.append("name", name);
    // formData.append("file[]", selectedFile);
    console.log(formData.get("file"), "<------- file");
    for (const pair of formData.entries()) {
      console.log(`${pair[0]}, ${pair[1]}`);
    }
    console.log("formData=======>", formData);

    axios({
      method: 'post',
      url: `${BASE_URL}/upload`,
      data: formData,
      headers: { 'Content-Type': 'multipart/form-data' }
    })
      .then(response => console.log(response))
      .catch(errors => console.log(errors));

    // axios
    //   .post(`${BASE_URL}/upload`,
    //     formData)
    //   .then((res) => {
    //     alert("File Upload success");
    //   })
    //   .catch((err) => alert("File Upload Error"));
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
        multiple
        onChange={(e) => setSelectedFiles(currFiles => [...currFiles, e.target.files])}
      />

      <button>Submit!</button>
    </form>
  );
}

export default FormFileTest;
