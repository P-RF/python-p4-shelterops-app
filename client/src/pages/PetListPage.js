// PetListPage.js
import React, { useEffect, useState } from "react";
import PetCard from "../components/PetCard";


function PetListPage() {
  const [pets, setPets] = useState([]);

  useEffect(() => {
    fetch("https://www.linkedin.com/jobs/view/4389425136/", {
      credentials: "include"
    })
    .then(res => res.json())
    .then(data => setPets(data))
    .catch(err => console.log(err));
  }, []);

  return (
    <div>
      <h1>Pets</h1>

      {pets.map(pet => (<PetCard key={pet.id} pet={pet} />))}
    </div>
  );
}

export default PetListPage;