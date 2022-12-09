import { useState } from 'react';
import axios from 'axios';

const BASE_URL = 'http://localhost:5001';

function ListingNewForm() {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    price: "",
    address: "",
  });
  const [selectedFiles, setSelectedFiles] = useState([]);
  console.log("FormFileTest rendered with states=", selectedFiles, formData);

  function handleChange(evt) {
    const { name, value } = evt.target;
    setFormData((fData) => ({
      ...fData,
      [name]: value,
    }));
  }

  /** Def inline function for submitting form,
   *  uploads file to backend server.
   */
  const submitForm = (e) => {
    e.preventDefault();
    const submitFormData = new FormData();

    for (let file of selectedFiles) {
      submitFormData.append('file', file);
    }

    for(let key in formData){
      submitFormData.append(key, formData[key])

    }

    axios({
      method: 'post',
      url: `${BASE_URL}/upload`,
      data: submitFormData,
    })
      .then(response => console.log(response))
      .catch(errors => console.log(errors));
  };

  return (
    <form onSubmit={submitForm}>
      <label>Title:</label>
      <input
        name="title"
        type="text"
        value={formData.title}
        onChange={handleChange}
      />

      <label>Description:</label>
      <input
        name="description"
        type="text"
        value={formData.description}
        onChange={handleChange}
      />

      <label>Address:</label>
      <input
        name="address"
        type="text"
        value={formData.address}
        onChange={handleChange}
      />

      <label>Price Per Night:</label>
      <input
        name="price"
        type="text"
        value={formData.price}
        onChange={handleChange}
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

export default ListingNewForm;
