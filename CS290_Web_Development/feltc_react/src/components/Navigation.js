// import dependencies
import React from 'react';
import { Link } from 'react-router-dom';

function Navigation() {
    return (
        /* if multiple nav, need unique id: <Navigation className="nav-1"> etc. */
        <nav>  
            <Link to="/">Home</Link>
            <Link to="../create-exercise">Add New Exercise</Link>

        </nav>

    );

}

export default Navigation;