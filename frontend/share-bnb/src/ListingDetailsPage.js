import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import ShareBnbApi from "./Api";


function ListingDetailsPage() {
  const { id } = useParams();
  const [listing, setListing] = useState(null);
  const [photos, setPhotos] = useState([]);

  console.log(
    "ListingDetailsPage rendered with",
    "listing=",
    listing,
    "photos=",
    photos,
  );

  useEffect(
    function loadListingsOnMount() {
      console.debug("ListingDetailsPage useEffect load", "listing=", listing);

      async function getOneListing() {
        const listing = await ShareBnbApi.getListing(id);
        setListing(() => listing);
        const photos = await ShareBnbApi.getListingPhotos(id);
        setPhotos(() => photos);
      }

      getOneListing();
    },
    []
  );

  return (
    <div className="ListingDetailsPage">
      {
        listing &&
        <div>
          <h2>{listing.title}</h2>
          <p>{listing.description}</p>
          {photos.map((p, idx) => (
            <img
              key={idx}
              src={p}
              alt={`${listing.title} #${idx}`}
            >
            </img>
          ))}
          <div>Address: {listing.address}</div>
          <div>Price: {listing.price}</div>
        </div>
      }
    </div>
  );

}

export default ListingDetailsPage;
