// PetListPage.js
import React, { useEffect, useState } from "react";
import PetCard from "../components/PetCard";


function PetListPage() {
  const [pets, setPets] = useState([]);

useEffect(() => {
  fetch("http://127.0.0.1:5555/pets", { credentials: "include" })
    .then(res => res.json())
    .then(data => {
      console.log("API data:", data);
      setPets(data);
    })
    .catch(err => console.log(err));
}, []);

  return (
    <div>
      <h1>Pets</h1>

      <div className="pet-grid">
        {pets.map(pet => (<PetCard key={pet.id} pet={pet} />))}
      </div>

    </div>
  );
}

export default PetListPage;