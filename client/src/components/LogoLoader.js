import React from "react";
import "./LogoLoader.css";
import logo from "../images/logo/shelterops-icon-bottle-no-background.png";

function LogoLoader() {
  return (
    <div className="loader-container">
      <div className="bottle-wrapper">
        <img src={logo} alt="ShelterOps loading" className="bottle" />
        <div className="pill pill1"></div>
        <div className="pill pill2"></div>
        <div className="pill pill3"></div>
        <div className="pill pill4"></div>
      </div>
      <p>Loading ShelterOps...</p>
    </div>
  );
}

export default LogoLoader;