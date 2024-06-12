from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta
from tinydb import TinyDB, Query
import pandas as pd
import string
import random
import json
app = Flask(__name__)

app._static_folder = './templates/static'
# Initialize TinyDB
db = TinyDB('db.json')

# Placeholder lists to store form data
start_times = []
total_hours = []
days = []

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/first')
def first():
    return render_template('basic.html')


@app.route('/save_form_data', methods=['POST'])
def save_form_data():
    data = request.json
    start_times.append(data['start_time'])
    #print(start_times)
    total_hours.append(data['total_hours'])
    #print(total_hours)
    days.extend(data['days'])
    #print(days)
    
    converted_data = {
    'start_time': start_times,
    'Total_Time': total_hours,
    'Days': days
    }
    #changed
    with open('basic.json', 'w') as file:
        # Write an empty dictionary to clear the file
        json.dump({}, file)
    
    print(converted_data)
    
    with open('basic.json', 'w') as file:
        json.dump(converted_data, file)
    
    # Accessing data from the JSON file
    with open('basic.json', 'r') as file:
        loaded_data = json.load(file)
    # Printing loaded data
    print("Loaded Data from JSON File:")
    print(loaded_data)

    # Accessing individual components
    start_time = loaded_data['start_time']
    total_time = loaded_data['Total_Time']
    day = loaded_data['Days']

    print("\nAccessed Components:")
    print("Start Time:", start_time)
    print("Total Time:", total_time)
    print("Days:", day)
    
    return jsonify({'message': 'Form data saved successfully'})

@app.route('/second')
def second():
    return render_template('mainform.html')


@app.route('/submit_form', methods=['POST'])
def submit_form():
    data = request.form.get('formData')
    if data:
        data = json.loads(data)
        #changed
        db.truncate()
        db.insert({'formData': data})
        return jsonify({'message': 'Form data submitted successfully'}), 200
    else:
        return jsonify({'error': 'No form data provided'}), 400
        

#Get the teachers and class data from the jason file

# Accessing data from the JSON file
with open('db.json', 'r') as file:
    loaded_data = json.load(file)
# Printing loaded data
print("Loaded Data from JSON File:")
print(loaded_data)

#This line is for getting basic info
# Accessing data from the JSON file
with open('basic.json', 'r') as file:
    loaded_data = json.load(file)
# Printing loaded data
print("Loaded Data from JSON File:")
print(loaded_data)

# Accessing individual components
start_time = loaded_data['start_time'][0]
total_time = loaded_data['Total_Time'][0]
#day = loaded_data['Days']

print("\nAccessed Components:")
print("Start Time:", start_time)
print("Total Time:", total_time)
#print("Days:", day)


def split_hours(start_time, total_hours):
    time_format = '%H:%M'
    hours = []

    # Convert start time string to datetime object
    start_datetime = datetime.strptime(start_time, time_format)

    for i in range(total_hours):
        # Calculate end time by adding one hour to the start time
        end_datetime = start_datetime + timedelta(hours=1)

        # Format start and end times as strings
        start_str = start_datetime.strftime(time_format)
        end_str = end_datetime.strftime(time_format)

        # Append formatted time range to the list
        hours.append(f"{start_str} - {end_str}")

        # Update start time for the next iteration
        start_datetime = end_datetime

    return hours

def replace_same_teacher(teachers, current_teacher):
    new_teacher = current_teacher
    while new_teacher == current_teacher:
        new_teacher = random.choice(teachers)
    return new_teacher

@app.route('/table')
def table():
    with open('db.json', 'r') as file:
        data = json.load(file)
    #This line is for getting basic info
    # Accessing data from the JSON file
    with open('basic.json', 'r') as file:
        loaded_data = json.load(file)
    # Printing loaded data
    print("Loaded Data from JSON File:")
    print(loaded_data)

    # Accessing individual components
    start_time = loaded_data['start_time'][0]
    total_time = loaded_data['Total_Time'][0]
    start_time = start_time
    total_hours = int(total_time)
    days_list = loaded_data['Days']
    time_ranges = split_hours(start_time, total_hours)

    # Parse JSON data
    class_data = data["_default"]["1"]["formData"]

    # Organize data into desired format
    organized_data = []

    for class_info in class_data:
        class_name = class_info["className"]
        teachers = class_info["teachers"]
        
        teacher_subjects = []
        for teacher in teachers:
            teacher_name = teacher["name"]
            subjects = teacher["subjects"]
            for subject in subjects:
                teacher_subjects.append(teacher_name + ' - ' + subject)
        
        class_dict = {'class': class_name, 'Teachers': teacher_subjects}
        organized_data.append(class_dict)

    # Create a dictionary to keep track of teacher replacements
    teacher_replacements = {}

    tables_data = []
    for class_info in organized_data:
        cls_nm = class_info['class']
        print(f'Class: {cls_nm}')
        teach = class_info['Teachers']

        column_names = time_ranges
        
        word_map = {}

        # Iterate over the list and assign each element to the dictionary with its index as the key
        for index, day in enumerate(days_list):
            word_map[index] = day

        #word_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3:'Thursday', 4:'Friday'}
        print(word_map)

        num_rows = len(word_map)

        df = pd.DataFrame(columns=column_names)

        
        for col in column_names:
            random_column = [replace_same_teacher(teach, teacher_replacements.get((col, day), None)) for day in word_map.values()]
            df[col] = random_column
            for i, day in enumerate(word_map.values()):
                teacher_replacements[(col, day)] = random_column[i]

        df = df.set_index(df.index.map(word_map))

        table = df.to_html(classes='center', escape=False)
        
        html_table = table.replace('<td>', '<td contenteditable="true">')

        tables_data.append({'class': cls_nm, 'table_data': html_table})

    return render_template('table.html', tables_data=tables_data)

if __name__ == '__main__':
    app.run(debug=True)

