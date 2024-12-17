# Name:
# Student ID:
# References (list any resources you've used in developing the code)
# e.g. - Flask documentation: https://flask.palletsprojects.com/en/stable/

import csv
import sqlite3
from pathlib import Path

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    url_for
)

app = Flask(__name__)

# Configuration
# The "Path.cwd()" function returns the current working directory. 
UPLOAD_FOLDER = Path.cwd() / 'uploads'
DB_FILE = Path.cwd() / 'data/iMusic.db'


####################
# Routes
####################

@app.route('/', methods=['GET'])
def index():
    """
    [No Need to Modify]
    Renders the home page.

    Returns:
        - The 'index.html' template.
    """
    return render_template('index.html')

@app.route('/upload/', methods=['GET', 'POST'])
def upload_route():
    """
    [No Need to Modify]

    Task 1: Handles file uploads for updating customer data.
    
    GET: Renders the upload page.
    POST: Processes the uploaded file, saves it, and updates the database.

    Returns:
        - Renders the upload.html template on GET.
        - Redirects to the index page on successful upload and database update.
    """
    if request.method == 'POST':
        # Retrieve the uploaded file
        file = request.files.get('file')
        if not file:
            flash('No file selected. Please upload a valid file.', 'warning')
            return redirect(url_for('upload_route'))

        # Define the path to save the uploaded file
        uploaded_file_path = UPLOAD_FOLDER / 'Customers.tsv'

        try:
            # Ensure the upload folder exists
            UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
            
            # Save the uploaded file
            file.save(uploaded_file_path)
            flash('File uploaded successfully.', 'success')

            # Update the database with the uploaded file
            update_customers(uploaded_file_path)
            flash('Customers updated successfully.', 'success')
        except Exception as e:
            # Handle errors during file saving or database update
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('upload_route'))

        # Redirect to the home page after successful upload
        return redirect(url_for('index'))

    # Render the upload page for GET requests
    return render_template('upload.html')

@app.route('/statistics/', methods=['GET', 'POST'])
def statistics():
    """
    [Incomplete]
    Task 2: Handles the statistics page.

    GET: Displays the statistics page.
    POST: Future functionality - handle country selection.

    Returns:
        - The 'statistics.html' template.
    """
    # You may need to modify or remove the following line of code
    return render_template('statistics.html')

@app.route('/invoice/', methods=['GET'])
def invoice():
    """
    [Incomplete]
    Task 3: Renders the invoice page.

    Returns:
        - The 'invoice.html' template.
    """
    # You may need to modify or remove the following line of code
    return render_template('invoice.html')

@app.route('/generate_invoice/', methods=['POST'])
def generate_invoice():
    """
    [Incomplete]
    Task 3: Handles invoice generation based on POST data.

    Returns:
        - The 'invoice.html' template after processing the request.
    """
    # Placeholder for future functionality

    # You may need to modify or remove the following line of code
    return render_template('invoice.html')

@app.errorhandler(404)
def page_not_found(e):
    """
    [No Need to Modify]
    Renders the error page for 404 errors.

    Returns:
        - The 'error.html' template with a 404 status code.
    """
    return render_template('error.html', messages=['404: Page not found.']), 404


####################
# Functions
####################

def update_customers(customer_tsv_file):
    """
    [Incomplete]
    Task 1: Update the customers table using the provided TSV file.

    Args:
        customer_tsv_file (Path): The path to the TSV file containing customer data to update.
    """
    # You will need to remove the pass statement and write your code here
    pass

def get_all_countries():
    """
    [Incomplete]
    Task 2: Retrieve all countries from the database.
    """
    # You will need to remove the pass statement and write your code here
    pass

def get_statistics(country):
    """
    [Incomplete]
    Task 2: Retrieve statistics for the specified country or all countries.

    Args:
        country (str): The country for which to retrieve statistics.
    """
    # You will need to remove the pass statement and write your code here
    pass

def get_all_customers():
    """
    [Incomplete]
    Task 3: Retrieve all customers from the database.
    """
    # You will need to remove the pass statement and write your code here
    pass

def get_all_albums():
    """
    [Incomplete]
    Task 3: Retrieve all albums from the database.
    """
    # You will need to remove the pass statement and write your code here
    pass

def process_invoice_in_db(customer_id, selections, address, city, country, postal_code):
    """
    [Incomplete]
    Task 3: Process the invoice in the database.

    Args:
        customer_id (int): The ID of the customer.
        selections (list): A list of album IDs selected by the customer.
        address (str): The customer's address.
        city (str): The customer's city.
        country (str): The customer's country.
        postal_code (str): The customer's postal code.
    """
    # You will need to remove the pass statement and write your code here
    pass


####################
# Main
####################

def main():
    """Run the Flask application."""
    app.secret_key = 'I love dbi'  # Secret key for session management
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    main()