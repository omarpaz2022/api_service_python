import json
import requests

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Tabla(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer)
    title = db.Column(db.String)
    completed= db.Column(db.String)

    def __repr__(self):
        return f"User ID: {self.userId} con titulo:{self.title} en estado: {self.completed}"


def add_row(userId, title, completed):
    # Cargar atributos en tabla
    row= Tabla(userId=userId, title=title, completed=completed)
    # Agregar fila a la Tabla_sql
    db.session.add(row)
    db.session.commit()
 

def fill():

    url = "https://jsonplaceholder.typicode.com/todos"
    data = requests.get(url).json()
 
    for row in data:
        userId= int(row.get("userId"))
        title= row.get("title")
        completed= row.get("completed")
        add_row(userId, title, completed)
    return


def title_completed_count(userId):
     # Crear la session
    cuenta = db.session.query(Tabla).filter(Tabla.userId == userId).filter(Tabla.completed == True).count()
    return(cuenta)



if __name__ == '__main__':

    # Crear una aplicación Flask para testing
    # y una base de datos fantasma (auxiliar o dummy)
    # Referencia:
    # https://stackoverflow.com/questions/17791571/how-can-i-test-a-flask-application-which-uses-sqlalchemy
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuario.db"
    # Bindear la DB con nuestra app Flask
    db.init_app(app)
    app.app_context().push()
    db.create_all()

    # Aquí se puede ensayar todo lo que necesitemos con nuestra DB

    fill()
    
    userId= input("Ingrese un userId del 1 al 10: ")
    cuenta= title_completed_count(userId)
    print(f"""El usuario userId=  {userId} tiene:
            cuenta titulos completos""")
   
    db.session.remove()
    db.drop_all()