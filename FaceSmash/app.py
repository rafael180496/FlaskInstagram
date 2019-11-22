from flask import (Flask, g, render_template, flash, url_for, redirect, abort)

from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, login_required, current_user,
                        logout_user, AnonymousUserMixin)
from FaceSmash import models,forms


DEBUG = True
PORT = 8000
HOST = '192.168.252.204'

app=Flask(__name__)
#llave de sesiones para crear y original de nuestra app
app.secret_key = 'ASFDXCYE!lfasdasd'';nljnAFON,.ASDOJJNLwuhebjlks23451'

#usuario anonimo
class Anonyimous(AnonymousUserMixin):
    def __init__(self):
        self.username='Invitado'

#instancia de login manager
    login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'#busca la vista de login en html

#usuario anonimo
login_manager.anonymous_user=Anonyimous







#carga los datos
#carga los datos del usuario
@login_manager.user_loader
def load_user(userid):
    try:
        # captura el usuario dependiendo la clase usuario que tenes
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


#antes de la peticion
@app.before_request
def before_request():
    """Conecta a la base de Datos antes de cada request"""
     #objeto g global
    # verifica si ya se habia conectado ala base de datos
    #if not hasattr(g,'db'):
    g.db = models.DATABASE
    # verifica si ya se habia conectado ala base de datos
    if g.db.is_closed():
        g.db.connect()
        g.user=current_user#se define de arriba desde flask login

#despues de la peticion

#se ejecuta despues de cada funcion
@app.after_request
def after_request(response):
    """Cerramos la conexión a la BD"""
    g.db.close()
    return response




#Seguir

@app.route('/follow/<string:username>')
@login_required
def follow(username):
    try:
        to_user=models.User.get(models.User.username**username)

    except models.DoesNotExist:
        pass

    else:
        try:
            models.Relationship.create(
                from_user=g.user._get_current_object(),
                to_user=to_user
            )
        except models.IntegrityError:
            abort(404)
        else:
            flash('Ahora sigues a  {}'.format(to_user.username),'success')
    return redirect(url_for('stream',username=to_user.username))


#dejar de seguir
@app.route('/unfollow/<string:username>')
@login_required
def unfollow(username):
    try:
        to_user=models.User.get(models.User.username**username)

    except models.DoesNotExist:
        abort(404)

    else:
        try:
            models.Relationship.get(
                from_user=g.user._get_current_object(),
                to_user=to_user
            ).delete_instance()
        except models.IntegrityError:
            abort(404)
        else:
            flash('Has dejado de seguir a {}'.format(to_user.username),'success')
    return redirect(url_for('stream',username=to_user.username))


#vistas

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash('Fuiste Registrado!!!', 'success')
        models.User.create_user(
            username = form.username.data,
            email = form.email.data,
            password= form.password.data
        )
        #rhidalgo
        # --------------------
        user = models.User.get(models.User.email == form.email.data)
        login_user(user)
        #--------------------
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


#mirar el post
@app.route('/post/<int:post_id>')
def view_post(post_id=0):
    posts=models.Post.select().where(models.Post.id ==post_id)

    if posts.count()==0:
        abort(404)

    return render_template('stream.html',stream=posts)



@app.route('/login',methods=('GET','POST'))
def login():
    form=forms.LoginForm()
    if form.validate_on_submit():
        try:
            user=models.User.get(models.User.email==form.email.data)

        except models.DoesNotExist:
            flash('Tu nombre de email o contraseña no existe','error')
        else:
            if check_password_hash(user.password,form.password.data):
                login_user(user)#inicia sesion
                flash('Has iniciado sesion','success')
                return redirect(url_for('index'))

    return render_template('login.html',form=form)



@app.route('/logout')
@login_required  #permite esta vista si el usuario ya esta logueado
def logout():
    logout_user()#termina la sesion del usuario
    flash('Has salido de FaceSmash','success')
    return redirect(url_for('index'))



@app.route('/new_post',methods=('GET','POST'))
@login_required
def post():
    form=forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(user=g.user._get_current_object()
                           ,content=form.content.data.strip())#usuario actual de la sesion
        flash('Mensaje posteado!','success')
        return redirect(url_for('index'))
    return render_template('post.html',form=form)




#pagina de inicio
@app.route('/')
def index():
    stream=models.Post.select().limit(100)
    return render_template('stream.html',stream=stream)


@app.route('/stream')
@app.route('/stream/<string:username>')
def stream(username=None):
    template='stream.html'

    if username and  username!= current_user.username:
        try:
            user=models.User.select().where(models.User.username**username).get()#** son como poner un like e ignorar
        except models.DoesNotExist:
            abort(404)#metodo de error
        else:
            stream=user.posts.limit(100)
    else:
        stream=current_user.get_stream().limit(100)
        user =current_user

    if username:
        template='user_stream.html'

    return  render_template(template,stream=stream,user=user)



@app.errorhandler(404)
def not_found(error):
    return  render_template('404.html'),404




if __name__ == '__main__':
    models.initialize()
    #usuario por defecto
    try:
        models.User.create_user(
            username='rafael',
            email='rafael180496@gmail.com',
            password='abc123',
        )
    except ValueError:
        pass
    app.run(debug=DEBUG,port=PORT,host=HOST)


