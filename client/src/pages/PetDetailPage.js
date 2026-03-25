// PetDetailPage.js
import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import MedicationLogItem from "../components/MedicationLogItem";

import "./PetDetailPage.css";

function PetDetailPage() {
  const {id} = useParams();
  const navigate = useNavigate();

  const [pet, setPet] = useState(null);
  const [logs, setLogs] = useState([]);

  // Fetch pet data
  useEffect(() => {
    fetch(`http://127.0.0.1:5555/pets/${id}`, {
      credentials: "include"
    })
    .then((res) => res.json())
    .then(setPet);

  // Fetch individual pet's medication logs
    fetch(`http://127.0.0.1:5555/medication_logs?pet_id=${id}`, {
      credentials: "include",
    })
      .then((res) => res.json())
      .then(setLogs);
  }, [id]);

  if (!pet) return <p>Loading...</p>

  const handleDeletePet = (petId) => {
    const confirmDelete = window.confirm("Are you sure you want to delete this pet?");

    if (!confirmDelete) return;

    fetch(`http://127.0.0.1:5555/pets/${petId}`, {
      method: "DELETE"
    })
      .then((res) => {
        if (res.ok) {
          alert("Pet deleted successfully!");
          navigate("/pets");
        } else {
          console.log("Failed to delete pet");
        }
      })
      .catch((error) => {
        console.log("Error deleting pet:", error);
      });
  };


  return (
    <div className="pet-detail-container">
      {/* Left panel */}
      <div className="pet-info-panel">
        <img
          src={pet.profile_image ? `http://127.0.0.1:5555/images/${pet.profile_image}` : "/images/placeholder-pet.png"}
          alt={pet.name}
          className="pet-detail-image"
        />

        <div className="pet-info">
          <p><strong>Name:</strong> {pet.name}</p>
          <p><strong>Breed:</strong> {pet.breed}</p>
          <p><strong>Age:</strong> {pet.age}</p>
          <p><strong>Sex:</strong> {pet.sex}</p>
          <p><strong>Weight:</strong> {pet.weight}</p>
          <p><strong>Date of Birth:</strong> {pet.date_of_birth}</p>
          <p><strong>DOB Estimated:</strong> {pet.dob_estimated}</p>
          <p><strong>Origin Location:</strong> {pet.origin_location}</p>
          <p><strong>Intake Date:</strong> {pet.intake_date}</p>
          <p><strong>Adoption Status:</strong> {pet.adoption_status}</p>
          <p><strong>Favorite Toy:</strong> {pet.favorite_toy}</p>
          <p><strong>Favorite Treat:</strong> {pet.favorite_treat}</p>

          <button 
            className="delete-pet-btn"
            onClick={() => handleDeletePet(pet.id)}
          >
            Delete Pet
          </button>
        </div>
      </div>
      {/* Right panel */}
      <div className="medication-panel">
        <h2>Medication History</h2>

        <div className="medication-list">
          {logs.map((log) => (<MedicationLogItem key={log.id} log={log}/>))}
        </div>

        <button className="add-medication-btn">+</button>
      </div> 
    </div>
  );
}

export default PetDetailPage;