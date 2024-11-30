from app import create_app, db
from app.models import User, Challenge

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Challenge': Challenge,
    }

if __name__ == '__main__':
    app.run(debug=True, port=8769, host='0.0.0.0')
