import { Link } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import { FaSun, FaMoon } from 'react-icons/fa';
import '../css/NavBar.css';

function NavBar() {
  const { isDark, toggleTheme } = useTheme();

  return (
    <nav>
      <h2>FineApp</h2>
      <ul>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/about">About</Link></li>
        <li><Link to="/contact">Contact</Link></li>
      </ul>
      <button className="theme-toggle" onClick={toggleTheme} aria-label="Toggle theme">
        {isDark ? <FaSun /> : <FaMoon />}
      </button>
    </nav>
  );
}

export default NavBar;