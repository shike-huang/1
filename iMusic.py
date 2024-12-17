# Name: Shike Huang
# Student ID:20617951
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
            flash(f'An error occurred: {str(e)}', 'danger')
            return redirect(url_for('upload_route'))

        return redirect(url_for('index'))

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
    countries = get_all_countries()
    selected_country = 'All'
    stats = []

    if request.method == 'POST':
        country = request.form.get('country')
        
        # Validate country selection
        if country not in countries:
            flash('Invalid country selected', 'danger')
            return redirect(url_for('statistics'))
        
        selected_country = country
        stats = get_statistics(country)
    
    return render_template('statistics.html', 
                           countries=countries, 
                           statistics=stats, 
                           selected_country=selected_country)

@app.route('/invoice/', methods=['GET'])
def invoice():
    """
    [Incomplete]
    Task 3: Renders the invoice page.

    Returns:
        - The 'invoice.html' template.
    """
    # You may need to modify or remove the following line of code
    customers = get_all_customers()
    albums = get_all_albums()
    return render_template('invoice.html', customers=customers, albums=albums)

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
    try:
        customer_id = request.form.get('customer')
        address = request.form.get('address')
        city = request.form.get('city')
        country = request.form.get('country')
        postal_code = request.form.get('postal_code')
        album_selections = request.form.getlist('albums')

        # Validate inputs
        if not customer_id or not album_selections:
            flash("Customer and albums must be selected.", "danger")
            return redirect(url_for('invoice'))

        # Process the invoice in the database
        process_invoice_in_db(
            customer_id=int(customer_id),
            selections=album_selections,
            address=address,
            city=city,
            country=country,
            postal_code=postal_code
        )

        flash("Invoice generated successfully.", "success")
        return redirect(url_for('invoice'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}", "danger")
        return redirect(url_for('invoice'))
    
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
    try:
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()

        # Open and read the TSV file
        with open(customer_tsv_file, 'r') as f:
            reader = csv.reader(f, delimiter='\t')  
            for row in reader:
                customer_id = row[0] if len(row) > 0 else None
                phone = row[9] if len(row) > 9 else None
                fax = row[10] if len(row) > 10 else None

                if not customer_id or not phone:
                    continue

                # Update the customer data if the CustomerId exists
                cursor.execute("SELECT 1 FROM Customer WHERE CustomerId = ?", (customer_id,))
                if cursor.fetchone():
                    if fax:
                        # Update both phone and fax
                        cursor.execute(
                            """
                            UPDATE Customer
                            SET Phone = ?, Fax = ?
                            WHERE CustomerId = ?
                            """,
                            (phone, fax, customer_id)
                        )
                    else:
                        # Update only the phone
                        cursor.execute(
                            """
                            UPDATE Customer
                            SET Phone = ?
                            WHERE CustomerId = ?
                            """,
                            (phone, customer_id)
                        ) 
        connection.commit()
        connection.close()
        flash('Customers updated successfully.', 'success')
    except Exception as e:
        flash(f'An error occurred while updating customers: {str(e)}', 'danger')

def get_all_countries():
    """
    [Incomplete]
    Task 2: Retrieve all countries from the database.
    """
    # You will need to remove the pass statement and write your code here
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    cursor.execute("SELECT DISTINCT Country FROM Customer")
    countries = [row[0] for row in cursor.fetchall()]
    countries.sort()
    
    connection.close()
    
    return ['All'] + countries

def get_statistics(country):
    """
    [Incomplete]
    Task 2: Retrieve statistics for the specified country or all countries.

    Args:
        country (str): The country for which to retrieve statistics.
    """
    # You will need to remove the pass statement and write your code here
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    # Query for all customers or specific country
    if country == 'All':
        cursor.execute("SELECT CustomerId, FirstName, LastName, Email, City FROM Customer")
    else:
        cursor.execute("SELECT CustomerId, FirstName, LastName, Email, City FROM Customer WHERE Country = ?", (country,))
    
    customers = cursor.fetchall()
    statistics = []
    total_invoices = 0
    total_amount = 0.0

    for customer in customers:
        customer_id, first_name, last_name, email, city = customer
        
        cursor.execute("SELECT COUNT(InvoiceId), COALESCE(SUM(Total), 0) FROM Invoice WHERE CustomerId = ?", (customer_id,))
        invoice_count, total_invoice_amount = cursor.fetchone()
        
        avg_amount = round(total_invoice_amount / invoice_count, 2) if invoice_count > 0 else 0.00
        
        # Add customer statistics to list
        statistics.append({
            'customer_id': customer_id,
            'name': f"{first_name} {last_name.upper()}",
            'email': email,
            'city': city,
            'number_of_invoices': invoice_count,
            'total_amount': round(total_invoice_amount, 2),
            'average_amount': avg_amount
        })
        
        # Update aggregated values
        total_invoices += invoice_count
        total_amount += total_invoice_amount

    connection.close()
    
    statistics.append({
        'customer_id': 'Total',
        'name': '',
        'email': '',
        'city': '',
        'number_of_invoices': total_invoices,
        'total_amount': round(total_amount, 2),
        'average_amount': round(total_amount / total_invoices, 2) if total_invoices > 0 else 0.00
    })
    
    return statistics


def get_all_customers():
    """
    [Incomplete]
    Task 3: Retrieve all customers from the database.
    """
    # You will need to remove the pass statement and write your code here
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT CustomerId, FirstName, LastName, Address, City, Country, PostalCode
        FROM Customer
        ORDER BY FirstName, LastName
    """)    
    customers = [
        {
            'customer_id': row[0],
            'name': f"{row[1]} {row[2].upper()}",
            'address': row[3] or '',
            'city': row[4] or '',
            'country': row[5] or '',
            'postal_code': row[6] or ''
        }
        for row in cursor.fetchall()
    ]

    connection.close()
    return customers

def get_all_albums():
    """
    [Incomplete]
    Task 3: Retrieve all albums from the database.
    """
    # You will need to remove the pass statement and write your code here
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT Album.AlbumId, Album.Title, Artist.Name, 9.99 AS Price
        FROM Album
        JOIN Artist ON Album.ArtistId = Artist.ArtistId
        ORDER BY Album.Title
    """)
    albums = [
        {
            'album_id': row[0],
            'title': row[1],
            'artist': row[2],
            'price': row[3]  # Static price
        }
        for row in cursor.fetchall()
    ]

    connection.close()
    return albums

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
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO Invoice (CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingCountry, BillingPostalCode, Total)
        VALUES (?, DATE('now'), ?, ?, ?, ?, ?)
    """, (customer_id, address, city, country, postal_code, len(selections) * 9.99))

    invoice_id = cursor.lastrowid

    for album_id in selections:
        cursor.execute("""
            INSERT INTO InvoiceLine (InvoiceId, TrackId, UnitPrice, Quantity)
            SELECT ?, TrackId, 9.99, 1
            FROM Track
            WHERE AlbumId = ?
            LIMIT 1
        """, (invoice_id, album_id))

    connection.commit()
    connection.close()



####################
# Main
####################

def main():
    """Run the Flask application."""
    app.secret_key = 'I love dbi'  # Secret key for session management
    app.run(debug=True, port=5000)


if __name__ == '__main__':
    main()