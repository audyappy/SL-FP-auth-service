import os

def set_db_uri(app, db_file_name):
    src_dir = os.path.abspath(os.path.dirname(__file__))
    project_dir = os.path.dirname(src_dir)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(project_dir, 'data', db_file_name)
    