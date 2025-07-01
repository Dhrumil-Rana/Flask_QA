from app import create_app
import os

#print("Current working directory:", os.getcwd())
#print("TEMPLATES DIR CONTENTS:", os.listdir("templates"))
#print("STATIC DIR CONTENTS:", os.listdir("app/static/css"))
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)