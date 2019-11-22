from peewee import  *
import datetime
import  sys
from collections import OrderedDict

db =SqliteDatabase('diary.db')



class Entry(Model):
    #fecha
    #content
    content =TextField()
    timestamp=DateTimeField(default=datetime.datetime.now)



    class Meta:
        database=db





def add_entry():
    """Registar una entrada en nuestro diario"""
    #documentacion
    print("Indroduce tu registro. Presiona Ctrl + D cuando termines")
    data=input()#sys.stdin.read().strip()

    if data:
        if input('Guardar entrada?[Yn]').lower() !='n':
            Entry.create(content=data)
            print('Guardada exitosamente')


def view_entries(query=None):
    """Despliega nuestra entradas"""
    #documentacion
    entries=Entry.select().order_by(Entry.timestamp.desc())

    if query:
        entries=entries.where(Entry.content.contains(query))

    for ent in entries:
       # tim=.strftime('A% %B %D, %Y %I:%M%p')
        print(ent.timestamp)
        print('****************************************')
        print(ent.content)
        print('****************************************')
        print('n| siguiente entrada')
        print('d| Borrar entrada')
        print('q| salir al menu')
        print('****************************************')
        next_action=input('Accion a realizar: [Nq]').lower().strip()

        if next_action =='q':
            break
        elif next_action =='d':
            delete_entry(ent)


def seatch_entries():
    """Buscar por cierto texto"""
    view_entries(input('Text a buscar:'))


def delete_entry(entry):
    """Borra un registro"""
    #documentacion

    resp=input("Estas seguro?[yN]").lower()
    if resp=='y':
        entry.delete_instance()
        print("Entrada borrada")



#menu ordenado
menu=OrderedDict([
    ('a',add_entry),
    ('v',view_entries),
    ('s',seatch_entries)

])


def menu_loop():
    """Muestra el menu"""
    #documentacion
    choice=None

    while choice!='q':#salir
        print("Presiona 'q' para salir")
        for key,value in menu.items():
            print('{}| {}'.format(key,value.__doc__))

        choice=input('Eleccion: ').lower().strip()
        if choice in menu:
            menu[choice]()



def initialize():
    db.connect()
    db.create_tables([Entry],safe=True)




if __name__=='__main__':
    initialize()
    menu_loop()




