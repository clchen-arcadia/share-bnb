import { useState, useEffect } from 'react';
import ListingCard from './ListingCard';

function ListingsPage() {
  const [listings, setListings] = useState([]);

  return (
    <div className="ListingsPage">
      ListingsPage
      <div className="ListingsPage-List">
        {listings.map((l) => (
            <ListingCard key={l.id} />
        ))}
      </div>
    </div>
  )
}

export default ListingsPage;
