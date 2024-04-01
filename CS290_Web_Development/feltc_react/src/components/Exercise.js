// import dependencies
import React from 'react';
// import icons
import { TiEdit } from "react-icons/ti";
import { RiDeleteBack2Fill } from "react-icons/ri";

function Exercise({ exercise, editExercise, deleteExercise}) {
    return (
        <tr>
            <td>{exercise.name}</td>
            <td>{exercise.reps}</td>
            <td>{exercise.weight}</td>
            <td>{exercise.unit}</td>
            <td>{exercise.date}</td>
            <td class="iconBorder">< TiEdit onClick={ () => editExercise(exercise) } 
                size="30px"
                onMouseOver={({target})=>target.style.color="white"}
                onMouseOut={({target})=>target.style.color="black"}/></td>
            <td class="iconBorder">< RiDeleteBack2Fill onClick={ () => deleteExercise(exercise._id) } 
                size="25px"
                onMouseOver={({target})=>target.style.color="white"}
                onMouseOut={({target})=>target.style.color="black"}/></td>
        </tr>
    );
}

export default Exercise;