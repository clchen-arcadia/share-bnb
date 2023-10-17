import { useNavigate } from 'react-router-dom';

function ListingCard({ listing }) {

  const navigate = useNavigate();

  function handleClick() {
    navigate(`/listings/${listing.id}`);
  }

  return (
    <div onClick={handleClick} className="ListingCard">
      <div className="card-body">
        <img
          src={listing.photo}
          alt={listing.title}
        />
        <h6>{listing.title}</h6>
        <p><small>{listing.description}</small></p>
      </div>
    </div>
  );
}

export default ListingCard;
