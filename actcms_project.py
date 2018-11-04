import os
from datetime import datetime
from flask import render_template, redirect, flash, session, Response
from forms import LoginForm, RegisterForm, PublishArtForm
from models import app, User, db
from werkzeug.security import generate_password_hash


# 登录
@app.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        session["user"] = data["name"]
        return redirect("/art/list/")  # 渲染模板
    return render_template("login.html", title="登录", form=form)  # 渲染模板


# 注册
@app.route('/register/', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data["name"],
            pwd=generate_password_hash(data["password"]),
            addtime=datetime.now()
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功!", "ok")
        return redirect("/login/")
    else:
        flash("输入注册信息", "err")
    return render_template("register.html", title="注册", form=form)  # 渲染模板


# 登出
@app.route('/logout/', methods=["GET"])
def logout():
    return redirect("/login/")  # 重定向到登录页面


# 发布文章
@app.route('/art/add/', methods=["GET", "POST"])
def art_add():
    form = PublishArtForm()
    return render_template("art_add.html", title="发布文章", form=form)  # 渲染模板


# 编辑文章
@app.route('/art/edit/<int:id>/', methods=["GET", "POST"])
def art_edit(id):
    return render_template("art_edit.html")  # 渲染模板


# 删除文章
@app.route('/art/del/<int:id>/', methods=["GET"])
def art_del(id):
    return redirect("/art/list/")  # 渲染模板


# 文章列表
@app.route('/art/list/', methods=["GET"])
def art_list():
    return render_template("art_list.html", title="文章列表")  # 渲染模板


# 验证码
@app.route('/codes/', methods=["GET"])
def codes():
    from codes import Code
    c = Code()
    info = c.create_code()
    # image = "static/code/{0}".format(info["img_name"]) # 用相对路径寸就用相对路径取
    image = os.path.join(os.path.dirname(__file__), "static/code") + "/" + info["img_name"]
    with open(image, "rb") as f:
        img = f.read()

    session["code"] = info["code"]
    return Response(img, mimetype="jpeg")


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5001)
