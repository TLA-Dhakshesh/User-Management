# User-Management

This is a Flask based API that provides inserting the JSON data to PostgresSQL and performing operartions like Pagination, searching, sorting, GET, PUT, PATCH, DELETE, POST.

# Clone the Repository
git clone https://github.com/TLA-Dhakshesh/User-Management.git

# Create a Virtual Environment
python -m venv myenv
source myenv/bin/activate

# Installations
pip install flask
pip install sqlalchemy psycopg2-binary

# Run these commands
export FLASK_APP=app.py
flask run

The API should now be running at http://127.0.0.1:5000/
## API Endpoint

## Get User
    Endpoint: GET /api/users
    Example:
    GET /api/users?page=1&limit=10&search=James&sort=-age

## Create User

    Endpoint: POST /api/users
    Example: 
    curl -X POST -F "file=@users.json" http://127.0.0.1:5000/api/users

## Get User by ID

    Endpoint: GET /api/users/<int:id>
    Example: 
    http://127.0.0.1:5000/api/users/4

## Update User

    Endpoint: PUT /api/users/<int:id>
    Example: 
    curl -X PUT "http://127.0.0.1:5000/api/users/1" \-H "Content-Type: application/json" \-d '{"first_name": "Dhakshesh", "last_name": "T L A", "company_name": "HPE", "city": 
            "Bangalore", "state":"KA", "zip":858, "email":"dhakshesh.t-l-a@hpe.com", "web":"www.hpe.com", "age":21}'

## Delete User

    Endpoint: DELETE /api/users/<int:id>
    Example: 
    http:127.0.0.1:5000/appi/users/499

## Partially Update User

    Endpoint: PATCH /api/users/<int:id>
    Example: 
    curl -X PATCH "http://127.0.0.1:5000/api/users/2" \-H "Content-Type: application/json" \-d '{"email": "xyz@google.com","age": 26}'

## Get User Summary

    Endpoint: GET /api/users/summary
    Example: 
    http://127.0.0.1:5000/api/users/summary

