// Navbar.js
import React from "react";
import { Link, useNavigate } from "react-router-dom";

function Navbar({ user, setUser}) {
  const navigate = useNavigate();

  function handleLogout() {
    fetch("http://127.0.0.1:5555/logout", {
      method: "DELETE",
      credentials: "include"
    })
    .then(res => {
      if (!res.ok && res.status !== 204) throw new Error("Logout failed");
      return res.json().catch(() => ({}));
    })
    .then(() => {
      setUser(null);
      navigate("/login", { replace: true });
    })
    .catch(err => console.log(err));
  }

  return (
    <nav>
      <h2>ShelterOps</h2>
      <div>
        <Link to="/">Dashboard</Link>
        <Link to="/pets">Pets</Link>
        <Link to="/medication_logs">Medication Logs</Link>
      </div>
      <div>
        <span>Welcome, {user?.name}</span>
        <button onClick={handleLogout}>
          Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;