// MedicationLogItem.js
import React from "react";

function MedicationLogItem( {log}) {
  return (
    <div className="medication-card">
      <button className="delete-medication">X</button>

      <p><strong>Medication:</strong> {log.medication_name}</p>
      <p><strong>Dosage:</strong> {log.dosage}</p>
      <p><strong>Given By:</strong> {log.given_by}</p>
      <p><strong>Date & Time:</strong> {log.time_given}</p>
      <p><strong>Medication Start Date:</strong> {log.start_date}</p>
      <p><strong>Medication End Date:</strong> {log.end_date}</p>
      <p><strong>Frequency:</strong> {log.frequency}</p>
      <p><strong>Notes:</strong> {log.notes}</p>
    </div>
  );
}

export default MedicationLogItem;