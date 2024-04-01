import React, { useState } from 'react';
import { useHistory } from "react-router-dom";

export const CreateExercisePage = () => {

    const [name, setName] = useState('');
    const [reps, setReps] = useState('');
    const [weight, setWeight] = useState('');
    const [unit, setUnit] = useState('lbs');  // default value is lbs *REQUIRED
    const [date, setDate] = useState('');
    
    const history = useHistory();

    // create a new exercise using the http method POST
    const createExercise = async () => {
        const newExercise = { name, reps, weight, unit, date };
        const response = await fetch('/exercises', {
            method: 'POST',
            body: JSON.stringify(newExercise),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        // successful requests will return a 201 response
        if(response.status === 201){
            alert("Added your new exercise!");
        } else {
            // log failed request and notify user
            console.error(`Failed to add the exercise, status code: ${response.status}`)
            alert("Could not add your exercise. Please try again.");
        }
        // automatically navigate page back to home when user dismisses the alert
        history.push("/");
    };

    return (
        <div>
            <h2>Add Exercise</h2>
            <p>Add a new exercise to the tracker. Enter the name, number of repetitions, 
                the weight (in pounds or kilograms), and the date you did the exercise.</p>
            <div class="form">
                <label for="name">Exercise Name</label>
                <input
                    id="name"
                    type="text"
                    placeholder="Deadlift"
                    value={name}
                    onChange={e => setName(e.target.value)} />
            </div>
            <div class="form">
                <label for="reps">Reps</label>
                <input
                    id="reps"
                    type="number"
                    placeholder="20"
                    style={{width: "55px"}}
                    value={reps}
                    onChange={e => setReps(e.target.value)} />
            </div>
            <div class="form">
                <label for="weight">Weight</label>
                <input
                    id="weight"
                    type="number"
                    placeholder="175"
                    style={{width: "55px"}}
                    value={weight}
                    onChange={e => setWeight(e.target.value)} />
            </div>
            <div class="form">
                <label for="units">Units</label>
                <select 
                    id="units"
                    value={unit} onChange={e => setUnit(e.target.value)}>
                    <option value="lbs">lbs</option>
                    <option value="kgs">kgs</option>
                </select>
            </div>
                <div class="form">
                <label for="date">Date</label>
                <input
                    id="date"
                    type="text"
                    value={date}
                    placeholder="MM-DD-YY"
                    size="8"
                    onChange={e => setDate(e.target.value)} />
            </div>
            <button
                onClick={createExercise}
            >Add</button>
        </div>
        
    );
}

export default CreateExercisePage;