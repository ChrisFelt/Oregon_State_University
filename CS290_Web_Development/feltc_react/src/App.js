// import styling
import './App.css';

// import dependencies
import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import { useState } from 'react';

// import pages
import HomePage from './pages/HomePage';
import CreateExercisePage from './pages/CreateExercisePage';
import EditExercisePage from './pages/EditExercisePage';

// import components
import Navigation from './components/Navigation.js';

// import logo
import { GiMuscleUp } from "react-icons/gi";

function App() {

    const [exerciseToEdit, setExerciseToEdit] = useState();

    return (
        <div className="App">
            <Router>
                <Navigation />

                <header className="App-header">
                    <GiMuscleUp className="App-logo" />
                    <GiMuscleUp className="App-logo2" />
                    <h1>Exercise Tracker</h1>
                    
                    <p>Track the exercises you've done! To add a new exercise, 
                        click on the add new exercise link above.</p>
                    <p>Once you've added an exercise, you can edit or delete it 
                        from the home page by clicking on the appropriate icon.</p>
                </header>

                <main>
                    <Route path="/" exact>
                        <HomePage setExerciseToEdit={setExerciseToEdit}/>
                    </Route>

                    <Route path="/create-exercise">
                        <CreateExercisePage />
                    </Route>

                    <Route path="/edit-exercise">
                        <EditExercisePage exerciseToEdit={exerciseToEdit} />
                    </Route>
                </main>
            </Router>

            <footer>
                <p>&copy; 2022 Christopher Felt</p>
            </footer>

        </div>
    );
}

export default App;