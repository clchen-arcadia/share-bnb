import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ListingCard from './ListingCard';
import ShareBnbApi from './Api';
import axios from 'axios';


function UsersListingsPage() {
  const { curr_user } = useParams();

  const [pageData, setPageData] = useState({
    data: null,
    isLoading: true,
  });
  console.log("UsersListingsPage rendered with pageData=", pageData);

  useEffect(
    function loadListingsOnMount() {
      // console.debug("ListingPage useEffect load", "pageData=", pageData);

      async function getUserListings() {
        const listings = await ShareBnbApi.getUserListings(curr_user);

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

      getUserListings();
    },
    [curr_user]
  );


  return (
    <div className="UsersListingsPage">
      <h1>
        My Listings
      </h1>
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
      <button>
        Add a Listing
      </button>
    </div>
  );
}

export default UsersListingsPage;
