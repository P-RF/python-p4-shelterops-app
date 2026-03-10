// Navbar.js
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav>
      <Link to="/">Dashboard</Link>
      <Link to="/pets">Pets</Link>
      <Link to="/medication_logs">Logs</Link>
    </nav>
  );
}

export default Navbar;