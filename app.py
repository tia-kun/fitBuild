from flask import Flask, render_template, send_from_directory, request, jsonify
from flask_cors import CORS
import os
import pandas as pd


# Create and enable CORS for the entire app
app = Flask(__name__, static_url_path='/my-workout-app/build', static_folder='my-workout-app/build')
CORS(app)

# Function to generate the workout plan based on user inputs
def generate_workout_plan(frequency, level, muscleGroup, workoutType):
    # Load the dataset
    df = pd.read_csv("/Users/tiakungwani/Downloads/megaGymDataset.csv")

    # Combining categories in the dataset
    combined_arms = ['Biceps', 'Triceps', 'Forearms']
    combined_shoulders = ['Traps', 'Shoulders']
    combined_back = ['Lats', 'Lower Back', 'Middle Back', 'Neck']
    combined_legs = ['Adductors', 'Abductors', 'Calves', 'Glutes', 'Hamstrings', 'Quadriceps']

    df['BodyPart'] = df['BodyPart'].replace(combined_arms, 'Arms')
    df['BodyPart'] = df['BodyPart'].replace(combined_shoulders, 'Shoulders')
    df['BodyPart'] = df['BodyPart'].replace(combined_back, 'Back')
    df['BodyPart'] = df['BodyPart'].replace(combined_legs, 'Legs')
    df['BodyPart'] = df['BodyPart'].replace('Abdominals', 'Abs')
    df['Type'] = df['Type'].replace('Strongman', 'Cardio')

    # Filter based on user inputs
    filtered_df = df[
        (df["Level"] == level) &
        (df["BodyPart"] == muscleGroup) &
        (df["Type"] == workoutType)
    ]

    # Generate workout plan for each day
    workout_plan = []
    for day in range(1, frequency + 1):
        # Check if there are enough exercises remaining in the dataset
        if len(filtered_df) < 6:
            print("Not enough data")
            break

        # Randomly choose 6 exercises and store them in a day-dataset
        day_df = filtered_df.sample(n=6)

        # Create a list with the retrieved exercise names
        exercises = day_df['Title'].tolist()

        # Remove the chosen exercises from the filtered dataset
        filtered_df = filtered_df.drop(day_df.index)

        # Append the exercise list to the workout plan
        workout_plan.append(f"Day {day}: {exercises}")

    return workout_plan


# Serve the React app and static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")
     #if path != "" and os.path.exists(os.path.join(os.path.dirname(__file__), "my-workout-app/build/" + path)):
       # return send_from_directory(os.path.join(os.path.dirname(__file__), "my-workout-app/build"), path)
    # else:
        # return send_from_directory(os.path.join(os.path.dirname(__file__), "my-workout-app/build"), "index.html")

# Home route
# @app.route('/')
# def index():
    # return render_template('index.html')

# Define route for the workout form
@app.route('/workout-form', methods=['POST'])
def workout_form():
    data = request.get_json() # Get the JSON data sent from the React frontend
    # print("Received data from frontend:", data)

    # Extract the relevant form data from the JSON
    frequency = int(data['frequency'])
    level = data['level'].capitalize()
    muscleGroup = data['muscle_group'].capitalize()
    workoutType = data['workout_type'].capitalize()

    # Call your workout program function here to generate the plan based on inputs
    workout_plan = generate_workout_plan(frequency, level, muscleGroup, workoutType)

    return jsonify(workout_plan)  # Return the generated workout plan as JSON

if __name__ == '__main__':
    app.run(debug=True)