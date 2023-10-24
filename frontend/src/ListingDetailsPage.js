import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import ShareBnbApi from "./Api";
import axios from "axios";


function ListingDetailsPage() {
  const { id } = useParams();

  const [pageData, setPageData] = useState({
    data: null,
    isLoading: true,
  });

  console.log(
    "ListingDetailsPage rendered with",
    "pageData=",
    pageData,
  );

  useEffect(
    function loadListingOnMount() {
      // console.debug("ListingDetailsPage useEffect load", "pageData=", pageData);

      async function getOneListing() {
        const listingPromise = ShareBnbApi.getListing(id);
        const photosPromise = ShareBnbApi.getListingPhotos(id);

        await axios.all([listingPromise, photosPromise]).then(axios.spread(function (listing, photos) {
          setPageData({
            data: { listing, photos },
            isLoading: false
          });
        }));
      }

      getOneListing();
    },
    [id]
  );

  return (
    <div className="ListingDetailsPage">
      {
        pageData.isLoading
          ? <p>Loading!</p>
          : <div>
            <h2>{pageData.data.listing.title}</h2>
            <p>{pageData.data.listing.description}</p>
            {pageData.data.photos.map((p, idx) => (
              <img
                className="listingImage"
                key={idx}
                src={p}
                alt={`${pageData.data.listing.title} #${idx}`}
              >
              </img>
            ))}
            <div>Address: {pageData.data.listing.address}</div>
            <div>Price: {pageData.data.listing.price}</div>
          </div>
      }
    </div>
  );

}

export default ListingDetailsPage;
