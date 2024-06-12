# Automatic-Timetable-Generator
## Overview

This project is a Flask-based web application designed to manage and display school timetables. It features the ability to input and store form data, generate class schedules, and present them in a user-friendly, editable HTML table format.
## Features

    Flask Web Framework: Utilizes Flask for routing and serving HTML templates.
    TinyDB: A lightweight, document-oriented database to store form data.
    JSON Handling: Reads and writes form data to JSON files for persistent storage.
    Dynamic Timetable Generation: Generates class schedules based on input data and displays them in an editable HTML table.
    User Interface: HTML templates for rendering web pages, including forms and tables.

## Dependencies

    Flask
    TinyDB
    Pandas
    JSON
    Python standard libraries: datetime, string, random

## Installation

    Clone the repository:

git clone https://github.com/Jared-Steven/Automatic-Timetable-Generator.git
cd flask-timetable-management

## Create and activate a virtual environment:

python -m venv venv

source venv/bin/activate  # On Windows use `venv\Scripts\activate`

## Install the required dependencies:

pip install -r requirements.txt

Run the application:

python app.py

## Open your web browser and go to:

    http://127.0.0.1:5000/

## File Structure

    app.py: Main application file containing the Flask routes and logic.
    templates/: Directory containing HTML templates.
        index.html: Home page template.
        basic.html: Template for displaying the first form.
        mainform.html: Template for displaying the second form.
        table.html: Template for displaying the generated timetable.
    static/: Directory for static files (CSS, JS, images).
    db.json: Database file for storing form data.
    basic.json: JSON file for storing start times, total hours, and days.

## Routes and Functionality

    Home Page ("/"):
        Renders index.html.

    Basic Form Page ("/first"):
        Renders basic.html.

    Save Form Data ("/save_form_data"):
        Method: POST
        Receives JSON data, stores it in lists, and writes it to basic.json.

    Main Form Page ("/second"):
        Renders mainform.html.

    Submit Form Data ("/submit_form"):
        Method: POST
        Receives form data, stores it in db.json.

    Generate Timetable ("/table"):
        Renders table.html with the generated timetable based on form data.

## Functions
split_hours(start_time, total_hours)

    Splits the given start time into hourly intervals based on the total hours.
    Parameters:
        start_time (str): The starting time in '%H:%M' format.
        total_hours (int): The total number of hours to split.
    Returns: A list of time ranges.

replace_same_teacher(teachers, current_teacher)

    Replaces a teacher with a different one to avoid consecutive slots being the same.
    Parameters:
        teachers (list): A list of available teachers.
        current_teacher (str): The current teacher to be replaced.
    Returns: A new teacher.

## Data Handling

    JSON Operations: Reads from and writes to basic.json and db.json for persistent storage.
    Data Conversion: Converts form data into a structured format suitable for timetable generation.
    Timetable Generation: Uses pandas to create a DataFrame, populates it with teacher schedules, and converts it to an HTML table.

## Example Usage

    Navigate to the Home Page:
        Access the basic form and main form pages from the home page.

    Submit Basic Form Data:
        Input start times, total hours, and days, then save the data.

    Submit Detailed Form Data:
        Input class and teacher details, then submit the form data.

    View Generated Timetable:
        View the dynamically generated timetable on the table page, with editable cells.

## License

This project is licensed under the MIT License.

Note: Make sure to adjust the paths and URLs according to your local setup and specific project details.
