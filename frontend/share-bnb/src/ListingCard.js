import { useNavigate } from 'react-router-dom';

// TODO: get bootstraps on the cards here
function ListingCard({ listing }) {

  const navigate = useNavigate();

  function handleClick() {
    navigate(`/companies/${listing.id}`);
  }

  return (
    <div onClick={handleClick} className="CompanyCard card">
      <div className="card-body">
        <h6>{listing.name}</h6>
        <p><small>{listing.description}</small></p>
        {listing.logoUrl &&
          <img
            src={listing.logoUrl}
            alt="logo"
            className="float-end ms-5 position-absolute top-0 end-0 p-2"></img>}
      </div>
    </div>
  );
}

export default ListingCard;
