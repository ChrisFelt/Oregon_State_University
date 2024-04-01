// import dependencies
import * as exercises from './exercises_model.mjs';
import express from 'express';

const PORT = 3000;
const app = express();

/**
 * REST API response is in JSON format
 */
app.use(express.json());

/**
 * Create a new exercise with name, reps, weight, unit, and date
 * Properties for the new exercise are contained in the body
 */
app.post('/exercises', (req, res) => {
    // try to create exercise with model function
    exercises.createExercise(req.body.name, req.body.reps, req.body.weight, req.body.unit, req.body.date)
        .then(exercise => {
            res.status(201).json(exercise);
        })
        .catch(error => {
            console.error(error);
            // Send a message in case of a 500 error
            res.status(500).json({ Error: 'Create new exercise request failed' });
        });

});

/**
 * Retrieve exercise using GET
 * Retrieves a single exercise using its unique id
 */
app.get('/exercises/:_id', (req, res) => {
    const exerciseId = { _id: req.params._id };
    // try to find exercise with model function
    exercises.findExerciseByID(exerciseId)
        .then(exercise => { 
            if (exercise !== null) {
                res.status(200).json(exercise);
            } else {
                res.status(404).json({ Error: 'Resource not found' });
            }         
         })
        .catch(error => {
            console.error(error);
            res.status(500).json({ Error: 'Retrieve by ID request failed' });
        });
});

/**
 * Retrieve all exercises using GET
 * Populates home page table
 */
app.get('/exercises', (req, res) => {
    // empty filter returns all exercises
    let filter = {};
    // try to find exercises with model function
    exercises.findExercises(filter)
        .then(exercises => {
            res.status(200).send(exercises);
        })
        .catch(error => {
            console.error(error);
            res.status(500).json({ Error: 'Retrieve all exercises request failed' });
        });
});

/**
 * Update an exercise using PUT
 * Updates the parameters (provided in the body) of an exercise given its unique id
 */
app.put('/exercises/:_id', (req, res) => {
    const exercise = { _id: req.params._id, name: req.body.name, reps: req.body.reps, 
        weight: req.body.weight, unit: req.body.unit, date: req.body.date }
    // try to update exercise with model function
    exercises.updateExercise(req.params._id, req.body.name, req.body.reps, req.body.weight, 
        req.body.unit, req.body.date)
        .then(modifiedCount => {
            // if modified count is 0, ID does not exist
            // otherwise, successfully updated the exercise
            if (modifiedCount === 1) {
                res.status(200).json(exercise)
            } else {
                res.status(404).json({ Error: 'Resource not found' });
            }
        })
        .catch(error => {
            console.error(error);
            res.status(500).json({ Error: 'Update request failed' });
        });
});

/**
 * Delete an exercise using DELETE
 * Delete the exercise with the given id
 */
app.delete('/exercises/:_id', (req, res) => {
    const deleteId = { _id: req.params._id };
    exercises.deleteExercise(deleteId)
        .then(deletedCount => {
            if (deletedCount === 1) {
                res.status(204).send();
            } else {
                res.status(404).json({ Error: 'Resource not found' });
            }
        })
        .catch(error => {
            console.error(error);
            res.status(500).json({ Error: 'Delete request failed' });
        });
});

app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
})
