import datetime

from flask_login import UserMixin
from flask_bcrypt import generate_password_hash

from peewee import *



DATABASE = SqliteDatabase('social.db')



#mixin agregar funcionalidad a otras clase


#usuarios
class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=120)
    joined_at =  DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    #devuelve todos los post de usuario
    def get_posts(self):
        return Post.select().where(Post.user==self)

    #devulve los post del usuario
    def get_stream(self):
        # opereadores or |
        return Post.select().where(
            (Post.user << self.following()) |
            (Post.user==self)
        )

    def following(self):
        """Los usuarios que estamos siguiendo"""
        return (
            User.select().join(
                Relationship,on=Relationship.to_user
            ).where(
                Relationship.from_user ==self#el usuario que inicio sesion
            )
        )

    def followers(self):
        """Obtener los usuarios que me siguen"""

        return (
            User.select().join(
                Relationship, on=Relationship.from_user
            ).where(
                Relationship.to_user == self  # el usuario que inicio sesion
            )
        )

    # metodo estatico
    @classmethod
    def create_user(cls, username, email, password):
        try:
            with DATABASE.transaction():#esta linea es una transaccion para hacer esta operacion
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                )


        except IntegrityError:
             raise ValueError('El usuario existe')




class Post(Model):
    user=ForeignKeyField(
        User,
        related_name='posts',
    )
    timestamp=DateTimeField(default=datetime.datetime.now)#cuando fue posteado
    content=TextField()

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)




class Relationship(Model):
    from_user=ForeignKeyField(User,related_name='relationships')
    to_user=ForeignKeyField(User,related_name='related_to')

    class Meta:
        database = DATABASE
        indexes=(# nos permite definir indices de la base de datos
            (('from_user','to_user'),True),
        )



def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User,Post,Relationship], safe=True)
    DATABASE.close()



