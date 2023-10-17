import { useState, useEffect } from 'react';
import ListingCard from './ListingCard';
import ShareBnbApi from './Api';

function ListingsPage() {
  const [listings, setListings] = useState([]);
  console.log("ListingsPages rendered with listings=", listings);

  useEffect(
    function loadListingsOnMount() {
      console.debug("ListingPage useEffect load", "listings=", listings);

      async function getAllListings() {
        const listings = await ShareBnbApi.getListings();
        setListings(() => listings);
      }

      getAllListings();
    },
    [listings]
  )

  return (
    <div className="ListingsPage">
      ListingsPage
      <div className="ListingsPage-List">
        {listings.map((l) => (
            <ListingCard key={l.id} listing={l} />
        ))}
      </div>
    </div>
  )
}

export default ListingsPage;
