import { useState, useEffect } from 'react';
import ListingCard from './ListingCard';
import ShareBnbApi from './Api';
import axios from 'axios';

function ListingsPage() {
  const [pageData, setPageData] = useState({
    data: null,
    isLoading: true,
  });
  console.log("ListingsPages rendered with pageData]=", pageData);

  useEffect(
    function loadListingsOnMount() {
      // console.debug("ListingPage useEffect load", "pageData]=", pageData);

      async function getAllListings() {
        const listings = await ShareBnbApi.getListings();

        const photoPromises = [];
        for (let i = 0; i < listings.length; i++) {
          const listing = listings[i];
          photoPromises.push(ShareBnbApi.getFirstPhoto(listing.id));
        }

        await axios.all(photoPromises).then(axios.spread(function (...photos) {
          for (let i = 0; i < listings.length; i++) {
            const listing = listings[i];
            listing.photo = photos[i];
          }
        }));

        setPageData({
          data: listings,
          isLoading: false,
        });
      }

      getAllListings();
    },
    []
  );

  return (
    <div className="ListingsPage">
      <h1>
        Listings
      </h1>
      <div className="ListingsPage-List">
        {
          pageData.isLoading
            ? <p>Loading!</p>
            : pageData.data.map(
              (l) => {
                return <ListingCard
                  key={l.id}
                  listing={l}
                />;
              })
        }
      </div>
    </div>
  );
}

export default ListingsPage;
