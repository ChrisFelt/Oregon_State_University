import React, { useState } from 'react';
import { useHistory } from "react-router-dom";

export const EditExercisePage = ( {exerciseToEdit} ) => {
    // initialize properties to the exercise that is being edited
    const [name, setName] = useState(exerciseToEdit.name);
    const [reps, setReps] = useState(exerciseToEdit.reps);
    const [weight, setWeight] = useState(exerciseToEdit.weight);
    const [unit, setUnit] = useState(exerciseToEdit.unit);
    const [date, setDate] = useState(exerciseToEdit.date);
    
    const history = useHistory();

    // update exercise using the http method PUT
    const editExercise = async () => {
        const exercise = { name, reps, weight, unit, date };
        const response = await fetch(`/exercises/${exerciseToEdit._id}`, {
            method: 'PUT',
            body: JSON.stringify( exercise ),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        // successful requests will return a 200 response
        if(response.status === 200){
            alert("Your exercise has been edited!");
        } else {
            // log failed request and notify user
            console.error(`Failed to edit the exercise, status code: ${response.status}`)
            alert("Could not edit your exercise. Please try again.");
        }
        // automatically navigate page back to home when user dismisses the alert
        history.push("/");
    };

    return (
        <div>
            <h2>Edit Exercise</h2>
            <p>Make any changes you wish to the exercise. Click save when you're done!</p>
            
            <div class="form">
                <label for="name">Exercise Name</label>
                <input
                    id="name"
                    type="text"
                    value={name}
                    onChange={e => setName(e.target.value)} />
            </div>
            <div class="form">
                <label for="reps">Reps</label>
                <input
                    id="reps"
                    type="number"
                    style={{width: "55px"}}
                    value={reps}
                    onChange={e => setReps(e.target.value)} />
            </div>
            <div class="form">
                <label for="weight">Weight</label>
                <input
                    id="weight"
                    type="number"
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
                    size="8"
                    onChange={e => setDate(e.target.value)} />
            </div>

            <button
                onClick={editExercise}
            >Save</button>
        </div>
    );
}

export default EditExercisePage;