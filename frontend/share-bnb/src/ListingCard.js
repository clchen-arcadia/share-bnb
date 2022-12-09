import { useNavigate } from 'react-router-dom';

function ListingCard({ listing }) {

  const navigate = useNavigate();

  function handleClick() {
    navigate(`/listings/${listing.id}`);
  }

  return (
    <div onClick={handleClick} className="ListingCard">
      <div className="card-body">
        <h6>{listing.title}</h6>
        <p><small>{listing.description}</small></p>
        <img
            src="test.com"
            alt={listing.title}
            className="float-end ms-5 position-absolute top-0 end-0 p-2"></img>
      </div>
    </div>
  );
}

export default ListingCard;
