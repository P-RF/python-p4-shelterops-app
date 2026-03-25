// PetCard.js
import React from "react";
import { useNavigate } from "react-router-dom";


function PetCard({ pet }) {
  const navigate = useNavigate();

  return (
    <div className="pet-card">
      <img 
        src={pet.profile_image ? `http://127.0.0.1:5555/images/${pet.profile_image}` : "/images/placeholder-pet.png"}
        alt={pet.name}
        className="pet-image"
      />

      <div className="pet-info">
        <p><strong>Name:</strong> {pet.name}</p>
        <p><strong>Breed:</strong> {pet.breed}</p>
        <p><strong>Age:</strong> {pet.age}</p>
        <p><strong>Status:</strong> {pet.status}</p>
        <p><strong>Favorite Toy:</strong> {pet.favorite_toy}</p>
        <p><strong>Favorite Treat:</strong> {pet.favorite_treat}</p>
      </div>

      <button
        className="view-details-btn"
        onClick={() => navigate(`/pets/${pet.id}`)}
      >
        View Details
      </button>

    </div>
  );
}

export default PetCard;