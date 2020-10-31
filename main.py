'''Main app file'''
from app import create_main_app

def app():
    '''create new app from factory'''
    app = create_main_app()
    return app

if __name__ == "__main__":
    newapp = app()
    newapp.run(debug=True, port=5000, host='0.0.0.0')
