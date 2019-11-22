from flask import  Flask,request,render_template

app=Flask(__name__)

@app.route('/')
def index():
    return "Hola mundo mi primera app de flask"


@app.route('/rafa')
def rafa(name='Mundo',apellido='todos'):
    #/rafa?name=dato&apellido=as
    name=request.args.get('name',name)
    apellido = request.args.get('apellido', apellido)
    return 'Hola '+name+' '+apellido



#url <name>
@app.route('/nombre/')
@app.route('/nombre/<string:name>/')
def nombre(name="app"):
    return  "Hola "+name



@app.route('/add/')
@app.route('/add/<int:num1>/')
@app.route('/add/<float:num1>/')
@app.route('/add/<int:num1>/<int:num2>/')
@app.route('/add/<float:num1>/<int:num2>/')
@app.route('/add/<int:num1>/<float:num2>/')
@app.route('/add/<float:num1>/<float:num2>/')
def add(num1=0,num2=0):
    return "La suma:{}".format(num1+num2)



#html
@app.route('/html/')
@app.route('/html/<string:nombre>/')
def html(nombre="Mundo"):
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document</title>
    </head>
    <body>
        <h1>Hola {}</h1>
    </body>
    </html>
    
    """.format(nombre)


@app.route('/temp/')
@app.route('/temp/<string:nombre>/')
def temp(nombre="Mundo"):
    return render_template('add.html',nombre=nombre)



#contexto
@app.route('/temp2/')
@app.route('/temp2/<string:nombre>/')
def temp2(nombre="Mundo"):
    context={'nombre':nombre} # se puede meter muchos valores y lo interpreta con llaves

    return render_template('add.html',**context)




#contexto
@app.route('/temp3/')
@app.route('/temp3/<string:nombre>/')
def temp3(nombre="Mundo"):
    context={'nombre':nombre} # se puede meter muchos valores y lo interpreta con llaves

    return render_template('index.html',**context)



app.run(debug=True,port=8000,host='0.0.0.0')




