// App.js
import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import LogoLoader from "./components/LogoLoader";

import DashBoardPage from "./pages/DashboardPage";
import LoginPage from "./pages/LoginPage";
import CreateAccountPage from "./pages/CreateAccountPage";
import PetlistPage from "./pages/PetListPage";
import PetDetailPage from "./pages/PetDetailPage";
import PetFormPage from "./pages/PetFormPage";
import MedicationLogsPage from "./pages/MedicationLogsPage";
import MedicationLogFormPage from "./pages/MedicationLogFormPage";

function App() {
  const [user, setUser] = useState(null); // Null = logged out
  const [loading, setLoading] = useState(true);

  // Automatically log user in if user has a session cookie
  useEffect(() => { 
    fetch("http://127.0.0.1:5555/check_session", {
      credentials: "include"
    })
    .then(res => (res.ok ? res.json() : null))
    .then(data => setUser(data))
    .catch(err => console.log(err))
    .finally(() => setLoading(false));
  }, []);
  
  if (loading) {
    return <LogoLoader />
  }

  return (
    <BrowserRouter>
    {user && <Navbar user={user} setUser={setUser} />}
      <Routes>
        {user ? (
          <>
            <Route path="/" element={<DashBoardPage />} />
            <Route path="/pets" element={<PetlistPage />} />
            <Route path="/pets/:id" element={<PetDetailPage />} />
            <Route path="/pets/new" element={<PetFormPage />} />
            <Route path="/medication_logs" element={<MedicationLogsPage />} />
            <Route path="/medication_logs/new" element={<MedicationLogFormPage />} />
          </>
        ) : (
          <>
            <Route path="/login" element={<LoginPage setUser={setUser} />} />
            <Route path="/signup" element={<CreateAccountPage setUser={setUser} />} />
            <Route path="*" element={<LoginPage setUser={setUser} />} />
          </>
        )}
      </Routes>
    </BrowserRouter>
  );
}


export default App;