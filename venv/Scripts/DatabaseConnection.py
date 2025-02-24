from flask_sqlalchemy import SQLAlchemy

server = r'DESKTOP-0UTQGQ1\SQLEXPRESS01'
database = 'DesafioBlog'
driver = 'ODBC+Driver+17+for+SQL+Server'

SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc://{server}/{database}?trusted_connection=yes&driver={driver}'

db = SQLAlchemy()
