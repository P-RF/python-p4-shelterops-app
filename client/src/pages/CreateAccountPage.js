// CreateAccountPage.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";


function CreateAccountPage({ setUser }) {
  const [username, setUsername] = useState("");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("Staff");
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();
    setError(null);

    fetch("http://127.0.0.1:5555/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ username, name, email, password, role })
    })
    .then(res => {
      if (!res.ok) {
        return res.json().then(data => {
          throw new Error(data.errors.join(", "));
        });
      }
      return res.json();
    })
    .then(user => {
      setUser(user);  // Log in immediately
      navigate("/");  // Go to dashboard
    })
    .catch(err => {
      setError(err.message);
    });
  }


  return (
    <div className="signup-page">
      <h1>Create Account</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}

      <form onSubmit={handleSubmit}>
        <input 
        type="text"
        placeholder="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
        required
        />
        <input 
          type="text"
          placeholder="Name"
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />
        <input 
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />

        <select value={role} onChange={e => setRole(e.target.value)}>
          <option value="admin">admin</option>
          <option value="staff">staff</option>
          <option value="volunteer">volunteer</option>
        </select>
        <button type="submit">Sign Up</button>
      </form>

      <p>
        Already have an account? <a href="/login">Login</a>
      </p>
    </div>
  );
}

export default CreateAccountPage;