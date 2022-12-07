import { useState } from 'react';
import axios from 'axios';

function FormFileTest() {
  const [name, setName] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);

  const submitForm = () => {
    const formData = new FormData();
    formData.append("name", name);
    formData.append("file", selectedFile);

    axios
      .post(UPLOAD_URL, formData)
      .then((res) => {
        alert("File Upload success");
      })
      .catch((err) => alert("File Upload Error"));
  };


  return (
    <form>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />

      <input
        type="file"
        value={selectedFile}
        onChange={(e) => setSelectedFile(e.target.files[0])}
      />
    </form>
  );
}

export default FormFileTest;
