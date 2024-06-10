from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pyodbc
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",  # Frontend origin
    "http://localhost:5500"
]

# Add CORS middleware to FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define a Pydantic model for the request body
class EmailRequest(BaseModel):
    email: str

# # Define a function to connect to your SQL Server database
def connect_db():
    server = 'LAPTOP-EEJ3525C\\SQLEXPRESS'
    database = 'AdventureWorks2019'
    username = 'somil'
    password = 'password'
    driver = '{ODBC Driver 17 for SQL Server}'  # Use appropriate driver
    
    # Create a connection string
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    # Connect to the database
    conn = pyodbc.connect(conn_str)
    return conn

# Define a route to handle the POST request from the frontend
@app.post('/query')
async def query_database(email_request: EmailRequest):
    email = email_request.email
    
    # Connect to the database
    conn = connect_db()
    cursor = conn.cursor()

    # Execute your SQL query to fetch the particular field based on the email
    cursor.execute("SELECT rowguid FROM [AdventureWorks2019].[Person].[EmailAddress] WHERE EmailAddress = ?", (email,))
    result = cursor.fetchone()
    
    # Check if result is None (email not found)
    if result is None:
        raise HTTPException(status_code=404, detail="Nahi Mil raha Bhai")
    
    # Close the database connection
    conn.close()

    return {'result': result[0]}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
