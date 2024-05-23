from app import db, app
from app.models import Admin
from werkzeug.security import generate_password_hash

def add_admin(username, password):
    with app.app_context():  # Adaugă această linie pentru a crea un context al aplicației
        # Crează un hash pentru parolă
        password_hash = generate_password_hash(password)
        
        # Crează un nou obiect Admin
        new_admin = Admin(username=username, password_hash=password_hash)
        
        # Adaugă noul admin în baza de date
        db.session.add(new_admin)
        try:
            db.session.commit()
            print("Admin added successfully.")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding admin: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python add_admin.py <username> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    password = sys.argv[2]
    add_admin(username, password)
