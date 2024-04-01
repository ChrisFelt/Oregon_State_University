// import mongoose db
import mongoose from 'mongoose';

// Create Exercise_db in the mongoDB server at default port
mongoose.connect(
    'mongodb://localhost:27017/exercises_db',
    { useNewUrlParser: true, useUnifiedTopology: true }
);

// Connect to db
const db = mongoose.connection;

// Log to console if connection successful
db.once('open', () => {
    console.log('Connection to database with Mongoose was successful.');
});

/**
 * Define exercises schema
 */
 const exerciseSchema = mongoose.Schema({
    name: { type: String, required: true},
    reps: { type: Number, required: true},
    weight: { type: Number, required: true},
    unit: { type: String, required: true},
    date: { type: String, required: true},
});

/**
 * Define Exercise model class
 */
const Exercise = mongoose.model("Exercise", exerciseSchema)

/**
 * **CREATE**
 * Define function for creating a new Exercise
 * @param {String} name 
 * @param {Number} reps
 * @param {Number} weight 
 * @param {String} unit
 * @param {String} date 
 * @returns a promise that resolves to a JSON object
 */
 const createExercise = async (name, reps, weight, unit, date) => {
    // create new instance of the Exercise class
    const exercise = new Exercise({name:name, reps:reps, weight:weight, unit:unit, date:date})

    // save the new Exercise to the database
    return exercise.save();
}

/**
 * **RETRIEVE 1**
 * Define function for finding a Exercise given the ID
 * @param {Object} id 
 * @returns a promise that resolves to a JSON object
 */
 const findExerciseByID = async (id) => {
    // create query object using id
    const query = Exercise.findOne(id);

    // call exec on the query object to retrieve search results
    return query.exec();
}

/**
 * **RETRIEVE MANY**
 * Define function for finding a Exercise given search parameters
 * @param {Object} filters 
 * @returns a promise that resolves to a JSON object
 */
 const findExercises = async (filters) => {
    // create query object using filters
    const query = Exercise.find(filters);

    // call exec on the query object to retrieve search results
    return query.exec();
}

/**
 * **UPDATE**
 * Define function for updating one or more properties of an Exercise
 * @param {String} id 
 * @param {String} name
 * @param {Number} reps
 * @param {Number} weight
 * @param {String} unit
 * @param {String} date
 * @returns a promise
 */
const updateExercise = async (id, name, reps, weight, unit, date) => {
    // call replaceOne model function
    const result = await Exercise.replaceOne({ _id: id}, { name: name, reps: reps, 
        weight: weight, unit: unit, date: date });

    // return the updated document
    return result.modifiedCount;
}

/**
 * **DELETE**
 * Define function for deleting an Exercise that matches a given property
 * @param {Object} condition (holds properties)
 * @returns a promise
 */
const deleteExercise = async (condition) => {
    // delete all Exercises that match the specified property
    const result = await Exercise.deleteOne(condition);
    
    // return number deleted
    return result.deletedCount;
}

// export functions for use in the controller
export {createExercise, findExerciseByID, findExercises, updateExercise, deleteExercise}