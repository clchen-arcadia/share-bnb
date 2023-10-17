import { useState, useEffect } from 'react';
import ListingCard from './ListingCard';
import ShareBnbApi from './Api';

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

        for (let i = 0; i < listings.length; i++) {
          const listing = listings[i];
          listing.photo = await ShareBnbApi.getFirstPhoto(listing.id);
        }

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
      ListingsPage
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
