import { useState } from 'react';
import './ListingNewForm.css';
import ShareBnbApi from './Api';
import { useContext } from 'react';
import userContext from './userContext';
import { useNavigate } from 'react-router-dom';
import Alert from './Alert';

const googleImgLink = 'https://www.google.com/search?q=airbnb%20room&tbm=isch&tbs=isz:i&hl=en&sa=X&ved=0CAQQpwVqFwoTCOCpt5aShYIDFQAAAAAdAAAAABAD&biw=1425&bih=758'

function ListingNewForm() {
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    price: "",
    address: "",
  });
  const [selectedFiles, setSelectedFiles] = useState([]);
  console.log("FormFileTest rendered with states=", selectedFiles, formData);

  const [errors, setErrors] = useState([]);

  const context = useContext(userContext);
  const username = context?.data?.username;

  const navigate = useNavigate();

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
  async function handleSubmit(evt) {
    evt.preventDefault();
    const submitFormData = new FormData();

    for (let file of selectedFiles) {
      submitFormData.append('file', file);
    }

    for (let key in formData) {
      submitFormData.append(key, formData[key]);
    }

    const res = await ShareBnbApi.postNewListing(username, submitFormData);

    console.warn("ERR=", res);

    if (res.errors !== undefined) {
      const errorMessages = [];
      for (let key in res.errors) {
        errorMessages.push(
          `${key}: ${res.errors[key]}`
        );
      }
      setErrors(errorMessages);
    }
    else if (res.success !== undefined) {
      alert('Success: created new listing');
      navigate(`/listings/user/${username}`);
    }
    else {
      setErrors(['Sorry, something went wrong']);
    }
  }


  return (
    <div>
      <form onSubmit={handleSubmit} className="NewListingForm d-flex flex-column">
        <label className="text-start">{`Title: (req.)`}</label>
        <input
          name="title"
          type="text"
          value={formData.title}
          onChange={handleChange}
        />

        <label className="text-start">{`Description: (req.)`}</label>
        <input
          name="description"
          type="text"
          value={formData.description}
          onChange={handleChange}
        />

        <label className="text-start">{`Address: (req.)`}</label>
        <input
          name="address"
          type="text"
          value={formData.address}
          onChange={handleChange}
        />

        <label className="text-start">{`Price Per Night: (req., number)`}</label>
        <input
          name="price"
          type="text"
          value={formData.price}
          onChange={handleChange}
        />

        <label className="text-start">{`Select File(s): (opt.)`}</label>
        <input
          type="file"
          multiple
          onChange={(e) => setSelectedFiles(() => e.target.files)}
        />

        <button>Submit!</button>
      </form>
      <p>Hint: Save an image from Google,
      <a
                href={googleImgLink}
                target="_blank"
                rel="noreferrer noopener"
                className='buttonExtA'
      >
      here
      </a>
      , to upload photo(s)</p>
      {errors.map((e, index) => <Alert key={index} err={e} />)}
    </div>
  );
}

export default ListingNewForm;
