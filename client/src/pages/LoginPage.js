// LoginPage.js
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function LoginPage({ setUser }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  function handleSubmit(e) {
    e.preventDefault();

    fetch("http://127.0.0.1:5555/login", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      credentials: "include",
      body: JSON.stringify({ username, password })
    })
    .then(res => {
      if (!res.ok) {
        throw new Error("Invalid username or password");
      }
      return res.json();
    })
    .then(user => {
      setUser(user);  // Store logged-in user
      navigate("/") // Go to dashboard
    })
    .catch(err => {
      setError(err.message);
    });
  }

  return (
    <div className="login-page">
      <h1>Login</h1>
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
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          required
        />

        <button type="submit">Login</button>
      </form>

      <p>
        Don't have an account? <a href="/signup">Sign Up</a>
      </p>
    </div>
  )
}

export default LoginPage;