import sqlite3 #build in libarary of python tow work with databases 
def get_connection(): #connects to the database
        return sqlite3.connect("entries.db")
def create_table():
        conn = get_connection() #opens a connection
        cursor = conn.cursor() #cursor lets u run commands on the database

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            date TEXT DEFAULT CURRENT_TIMESTAMP
        ) 
    """) #the commands
        conn.commit() # saves the changes to the database 
        conn.close() #closes the connection after saving changes
def save_entry(content):
        conn = get_connection() #opens a new connection
        cursor = conn.cursor() #creates a cursor to execute commands
        cursor.execute("INSERT INTO entries (content) values (?)", (content,)) #executes a command to insert a new entry into the database, the content is passed as a parameter to prevent SQL injection
        conn.commit() # saves the changes to the database
        entry_id = cursor.lastrowid # gets the id of the last inserted entry
        conn.close()# closes the connection after saving the changes to the database
        return entry_id
def get_entries():
    con = get_connection() # opens a new connection
    cursor = con.cursor() #creates a cursor to execute commands
    cursor.execute("SELECT id, content, date FROM entries ORDER BY date DESC") # executes a command to retrieve all entries ordered by date
    entries = cursor.fetchall() #fetches all the results of the executed commands
    con.close() #closes the connection after fetching the results
    return entries #returns the entries out of the funtion 
