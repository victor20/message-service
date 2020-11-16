import os
os.environ['DATABASE_URL'] = 'sqlite:///../site.db'

from messageservice import app, db

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)



