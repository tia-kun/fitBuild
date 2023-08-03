import React, { useState } from 'react';
import axios from 'axios';

const WorkoutForm = () => {
  const [frequency, setFrequency] = useState('');
  const [level, setLevel] = useState('');
  const [muscleGroup, setMuscleGroup] = useState('');
  const [workoutType, setWorkoutType] = useState('');
  const [workoutPlan, setWorkoutPlan] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const data = {
      frequency,
      level,
      muscle_group: muscleGroup,
      workout_type: workoutType,
    };

    /* const formData = new FormData();
      formData.append('frequency', frequency);
      formData.append('level', level);
      formData.append('muscle_group', muscleGroup);
      formData.append('workout_type', workoutType); */

    try {
      // Make a POST request to your Flask backend endpoint for workout plan generation
      const response = await axios.post('/workout-form', data);
      setWorkoutPlan(response.data); // Update state with the generated workout plan
    } catch (error) {
      console.error('Error generating workout plan:', error);
    }
  };

  return (
    <div>
      <h1>Customized Workout Plan</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="frequency">Number of days per week:</label>
        <input type="number" name="frequency" value={frequency} onChange={(e) => setFrequency(e.target.value)} required />
        <label htmlFor="level">Fitness level:</label>
        <input type="text" name="level" value={level} onChange={(e) => setLevel(e.target.value)} required />
        <label htmlFor="muscleGroup">Targeted muscle group:</label>
        <input type="text" name="muscleGroup" value={muscleGroup} onChange={(e) => setMuscleGroup(e.target.value)} required />
        <label htmlFor="workoutType">Workout type:</label>
        <input type="text" name="workoutType" value={workoutType} onChange={(e) => setWorkoutType(e.target.value)} required />
        <button type="submit">Generate Workout Plan</button> {/* Add the button for form submission */}
      </form>

      {/* Display the generated workout plan */}
      {workoutPlan && (
        <div>
          <h2>Generated Workout Plan</h2>
          <ul>
            {Object.keys(workoutPlan).map((day) => (
              <li key={day}>
                <strong>{day}:</strong>
                <ul>
                  {workoutPlan[day].map((exercise, index) => (
                    <li key={index}>{exercise}</li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default WorkoutForm;

