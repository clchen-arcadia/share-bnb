import axios from 'axios';
import { useState } from 'react';

const BASE_URL = 'http://localhost:5001';


function GetAndDisplayImage() {
  const [pics, setPics] = useState([]);
  async function handleClick() {
    const resp = await axios({
      url: `${BASE_URL}/pics`,
      method: 'GET',
    });

    console.log("TEST>>>>> resp.data is", resp.data);

    setPics(() => resp.data.contents);
  }

  return (
    <div className="GetAndDisplayImage">
      <button onClick={handleClick}>Get Images!</button>
      <section id="section-photos">
        {
          pics.map((p, idx) => {
            console.log("p=", p);
            return <img key={idx} src={p} alt={p}/>;
          })
        }
      </section>
    </div>
  );
}


export default GetAndDisplayImage;
