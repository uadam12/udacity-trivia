import { Link } from 'react-router-dom';
import React from 'react';
import '../stylesheets/Header.css';

const Header = () => 
(<nav className='navbar'>
  <div className='logo'>
    <Link to="/">Udacitrivia</Link>
  </div>

  <div className="nav-links">
    <input type="checkbox" id="checkbox_toggle" />
    <label htmlFor='checkbox_toggle' className='hamburger'>&#9776;</label>

    <ul className='menu'>
        <li>
            <Link to="/">List</Link>
        </li>

        <li>
            <Link to="add">Add</Link>
        </li>

        <li>
            <Link to="play">Play</Link>
        </li>
    </ul>
  </div>
</nav>);

export default Header;
