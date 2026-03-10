// App.js
import React, { useState } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar"


import DashBoardPage from "./pages/DashboardPage"
import LoginPage from "./pages/LoginPage"
import CreateAccountPage from "./pages/CreateAccountPage"
import PetlistPage from "./pages/PetListPage"
import PetDetailPage from "./pages/PetDetailPage"
import PetFormPage from "./pages/PetFormPage"
import MedicationLogsPage from "./pages/MedicationLogsPage"
import MedicationLogFormPage from "./pages/MedicationLogFormPage"

function App() {
  const [user, setUser] = useState(null); // Null = logged out

  return (
    <BrowserRouter>
      <Navbar user={user} setUser={setUser} />

      <Routes>
        <Route path="/" element={<DashBoardPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<CreateAccountPage />} />
        <Route path="/pets" element={<PetlistPage />} />
        <Route path="/pets/:id" element={<PetDetailPage />} />
        <Route path="/pets/new" element={<PetFormPage />} />
        <Route path="/medication_logs" element={<MedicationLogsPage />} />
        <Route path="/medication_logs/new" element={<MedicationLogFormPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;