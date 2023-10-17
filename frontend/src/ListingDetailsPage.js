import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import ShareBnbApi from "./Api";


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
    function loadListingsOnMount() {
      // console.debug("ListingDetailsPage useEffect load", "pageData=", pageData);

      async function getOneListing() {
        const listing = await ShareBnbApi.getListing(id);
        const photos = await ShareBnbApi.getListingPhotos(id);

        setPageData({
          data: { listing, photos },
          isLoading: false
        })
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
