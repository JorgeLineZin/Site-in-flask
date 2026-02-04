from flask import render_template, url_for, redirect
from principal import app, database, bcrypt
from flask_login import login_required, logout_user, login_user, current_user
from principal.forms import FormLogin, FormRegistro, FormPost
from principal.models import User, Post


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    formlogin = FormLogin()
    if formlogin.validate_on_submit():
        user = User.query.filter_by(email=formlogin.email.data).first()
        if user and bcrypt.check_password_hash(user.password, formlogin.password.data):
            login_user(user, remember=True)
            return redirect(url_for("perfil", id_user=user.id))
    return render_template("login.html", form=formlogin)


@app.route("/register", methods=["GET", "POST"])
def register():
    formregistro = FormRegistro()
    if formregistro.validate_on_submit():
        password_hashed = bcrypt.generate_password_hash(formregistro.password.data)
        user = User(
            name=formregistro.username.data,
            email=formregistro.email.data,
            password=password_hashed,
        )
        database.session.add(user)
        database.session.commit()
        login_user(user, remember=True)
        return redirect(url_for("perfil", id_user=user.id))
    return render_template("register.html", form=formregistro)


@app.route("/perfil/")
@login_required
def perfil_user():
    return redirect(url_for("perfil", id_user=current_user.id))


@app.route("/perfil/<id_user>", methods=["GET", "POST"])
@login_required
def perfil(id_user):
    form_post = FormPost()
    if form_post.validate_on_submit():
        post = Post(
            title=form_post.title.data,
            content=form_post.content.data,
            id_user=current_user.id,
        )
        database.session.add(post)
        database.session.commit()
        return redirect(url_for("perfil", id_user=current_user.id))
    if int(id_user) == int(current_user.id):
        return render_template(
            "perfil.html", username=current_user, form_post=form_post
        )
    else:
        username = User.query.get(int(id_user))
        if username is None:
            return redirect(url_for("index"))
        return render_template("perfil.html", username=username, form_post=form_post)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
