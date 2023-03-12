import traceback 
from flask import Flask, request, jsonify, render_template, Response, redirect 
import graph 
import usuario 




# Crear el server Flask
app = Flask(__name__)

# Indicamos al sistema (app) de donde leer la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///usuario.db"
# Asociamos nuestro controlador de la base de datos con la aplicacion
usuario.db.init_app(app)

# Ruta que se ingresa por la ULR 127.0.0.1:5000
@app.route("/")
def index():
    try:
        # Imprimir los distintos endopoints disponibles
        result = "<h1>Ejercicio de profundizacion..</h1>"
        result += "<h2>Endpoints disponibles:</h2>"
        result += "<h3>[GET] /user/{id}/titles ---> Esta ruta es la encargada a informar al solicitante cuantos titulos completó un usuario(1 al 10).</h3>"
        result += "<h3>[GET] /user/graph ---> Esta ruta es la encargada de informar el reporte y comparativa de cuantos títulos completó cada usuario en un gráfico.</h3>"
        result += "<h3>[GET] /user/titles ---> Esta ruta es la encargada a informar cuantos títulos completó cada usuario en un JSON.</h3>"
        return(result)
    except:
        return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000/user/<userId>/titles
@app.route("/user/<userId>/titles")
def titulos_completos(userId):
    try:
        # Obtener de la BD los titulos completados del userId  
        cuenta = usuario.title_completed_count(userId)
        return jsonify(cuenta)
    except:
        return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000/user/graph
@app.route("/user/graph")
def grafica():
    try:
        users=[]
        titles_ap=[]
        for x in range(1,11):
            cuenta = usuario.title_completed_count(x)
            titles_ap.append(cuenta)
            users.append(x)
        # Transformar los datos en una imagen HTML con matplotlib
        image_html = graph.graficar(users, titles_ap)
        return Response(image_html.getvalue(), mimetype='image/png')
    except:
        return jsonify({'trace': traceback.format_exc()})


# Ruta que se ingresa por la ULR 127.0.0.1:5000/user/titles
@app.route("/user/titles")
def titles_json():
        tit_json=[]
        for x in range(1,11):
            cuenta = usuario.title_completed_count(x)
            #titles_ap.append(cuenta)
            #users.append(x)
            tit_json.append({"Usuario": x, "Titulos completos": cuenta})
        return jsonify(tit_json)


# Este método se ejecutará solo una vez
# la primera vez que ingresemos a un endpoint
@app.before_first_request
def before_first_request_func():
    # Borrar y crear la base de datos
    usuario.db.drop_all()
    usuario.db.create_all()
    # Completar la base de datos
    usuario.fill()
    print("Base de datos generada")
    


if __name__ == '__main__':
    
    # Lanzar server
    app.run(host="127.0.0.1", port=5000)
