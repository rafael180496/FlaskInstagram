from peewee import *

#base de datos sqllite
db = SqliteDatabase('estudiante.db')

#modelos


class Estudiante(Model):
    username=CharField(max_length=255,unique=True)#tipo texto
    puntos=IntegerField(default=0)

    #clase meta dentro
    # se le indica a que clase de base datos es
    class Meta:
        database=db



listaEstudiante=[
    {
        'username':"aldo",
        'puntos':10
    },{
        'username':"pedro",
        'puntos':9
    },{
        'username':"rafa",
        'puntos':6
    },{
        'username':"paco",
        'puntos':5
    },{
        'username':"kevin",
        'puntos':1
    },
]



def top_estudiante():
    est=Estudiante.select().order_by(Estudiante.puntos.desc()).get() # solo obtiene el mas alto y un solo registro
    return est

def agregarEstudiante():
    for est in listaEstudiante:

        try:
            Estudiante.create(username=est['username'],puntos=est['puntos'])
        except IntegrityError:
            estudiante_recor=Estudiante.get(username=est['username'])
            estudiante_recor.puntos=est['puntos']
            estudiante_recor.save()

if  __name__=='__main__':
    db.connect()# conecta cada vez
    db.create_tables([Estudiante],safe=True)#si se ejecuta una vex si ya esta creado
    #agregarEstudiante()
    est=top_estudiante()
    print('El mejor estudiante es:{} con un puntaje de :{}'.format(est.username,est.puntos))