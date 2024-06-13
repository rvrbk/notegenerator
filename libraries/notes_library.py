import sqlite3, os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class NotesLibrary():
    connection = None
    cursor = None
    
    def __init__(self):
        os.makedirs(os.path.dirname('data/data.db'), exist_ok=True)
        
        try:
            self.connection = sqlite3.connect('data/data.db')
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
        except sqlite3.Error as error:
            print(error)
            
    def create_notes_table(self) -> bool:
        result = False
        
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
            create table if not exists notes(
                id integer primary key autoincrement,
                title text not null,
                content text not null,
                release not null,
                external_id text not null,
                created text not null
            )                
            """)
            
            result = True
        except sqlite3.Error as error:
            print(error)
        finally:
            if self.connection:
                self.cursor.close()
                self.connection.close()
            
        return result
            
        
    def insert_note(self, item, notes) -> bool:
        result = False
        
        try:
            insert_query = """
            INSERT INTO notes (title, content, release, external_id, created) 
            VALUES (?, ?, ?, ?, ?)
            """
            self.cursor.execute(insert_query, (
                notes['title'],
                notes['notes'],
                os.environ.get('RELEASE', 'default_release'),
                str(item.key),
                datetime.now().isoformat()
            ))
            
            self.connection.commit()
            
            result = True
        except sqlite3.Error as error:
            print(error)
        finally:
            if self.connection:
                self.cursor.close()
                self.connection.close()
            
        return result
    
    def get_notes(self, release=None):
        result = False
        
        try:
            query = """
            SELECT * FROM notes
            """
            
            if release:
                query += " WHERE release = ?"
            
                self.cursor.execute(query, (release,))
            else:
                self.cursor.execute(query)
            
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as error:
            print(error)
        finally:
            if self.connection:
                self.cursor.close()
                self.connection.close()
            
        return result