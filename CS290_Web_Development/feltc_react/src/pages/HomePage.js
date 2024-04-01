// import dependencies
import React from 'react';
import ExerciseTable from '../components/ExerciseTable';
import { useState, useEffect } from 'react';
import { useHistory } from 'react-router-dom';

function HomePage( {setExerciseToEdit} ) {
    const [exercises, setExercises] = useState([]);
    const history = useHistory();

    // send a get request to localhost:3000/exercises to retrieve the exercises from the db
    // default http method for fetch is GET
    const loadExercises = async () => {
        const response = await fetch('/exercises');
        const exercises = await response.json();
        setExercises(exercises);
    };
    
    // useEffect can't contain an async function, so we pass it as the variable loadExercises
    useEffect(() => {
        loadExercises();
    }, []);

    // send a DELETE request to localhost:3000/exercises to delete an exercise from the db
    // invoked when the delete button is clicked
    const deleteExercise = async id => {
        const response = await fetch(`/exercises/${id}`, { method: 'DELETE' });
        // a status code of 204 indicates the item was deleted successfully
        if (response.status === 204) {
            // reload exercises from the updated db using GET request
            const getResponse = await fetch('/exercises');
            const exercises = await getResponse.json();
            setExercises(exercises);
        } else {
            console.error(`Request to delete exercise with id: ${id} failed. Status code: ${response.status}`)
        }
    };

    // send a PUT request to localhost:3000/exercises/:_id to edit an exercise
    const editExercise = exercise => {
        setExerciseToEdit(exercise);
        history.push("/edit-exercise");
    };

    return (
        <>
            <h2>Your Exercises</h2>
            <ExerciseTable exercises={exercises} editExercise={editExercise} deleteExercise={deleteExercise}></ExerciseTable>
        </>
    );
}

export default HomePage;