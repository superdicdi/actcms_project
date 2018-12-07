import os
import uuid
from datetime import datetime
from functools import wraps

from flask import render_template, redirect, flash, session, Response, url_for, request
from forms import LoginForm, RegisterForm, PublishArtForm, EditArtForm
from models import app, User, db, Art
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
app.config["UP"] = os.path.join(os.path.dirname(__file__), "static/uploads")

def user_login(f):
    @wraps(f)
    def login_req(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return login_req


# 登录
@app.route('/login/', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        session["user"] = data["name"]
        return redirect("/art/list/1/")  # 渲染模板
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
@user_login
def logout():
    session.pop("user", None)
    return redirect("/login/")  # 重定向到登录页面


# 修改文件名称
def change_name(name):
    info = os.path.splitext(name)
    print(info)
    # 文件名：时间格式字符串+唯一字符串+后缀名
    name = datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + info[-1]
    return name


# 发布文章
@app.route('/art/add/', methods=["GET", "POST"])
@user_login
def art_add():
    form = PublishArtForm()
    if form.validate_on_submit():
        data = form.data
        print(form.logo.data.filename)
        file = secure_filename(form.logo.data.filename)
        print("file == ", file)
        logo = change_name(file)
        print("logo == ", logo)
        if not os.path.exists(app.config["UP"]):
            os.makedirs(app.config["UP"])

        form.logo.data.save(app.config["UP"] + "/" + logo)
        user = User.query.filter_by(name=session["user"]).first()
        user_id = user.id
        # 保存数据
        art = Art(
            title=data["title"],
            cate=data["category"],
            user_id=user_id,
            logo=logo,
            content=data["content"],
            addtime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        db.session.add(art)
        db.session.commit()

    return render_template("art_add.html", title="发布文章", form=form)  # 渲染模板


# 编辑文章
@app.route('/art/edit/<int:id>/', methods=["GET", "POST"])
@user_login
def art_edit(id):
    form = EditArtForm()
    form.logo.validators = []  # 取消非空约束，当用户未上传图片时不提示，默认用上一次上传的图片
    art = Art.query.get_or_404(int(id))

    if request.method == "GET":  # get 进来赋默认值，此时 form.logo.data = logo名.jpg
        form.content.data = art.content
        form.category.data = art.cate
        form.logo.data = art.logo

    if form.validate_on_submit():

        data = form.data
        art.title = data["title"]
        if not os.path.exists(app.config["UP"]):
            os.makedirs(app.config["UP"])

        if hasattr(form.logo.data, "filename"):
            file = secure_filename(form.logo.data.filename)
            art.logo = change_name(file)
            form.logo.data.save(app.config["UP"] + "/" + art.logo)

        art.cate = data["category"]
        art.content = data["content"]
        db.session.add(art)
        db.session.commit()
    return render_template("art_edit.html", form=form, title="编辑文章", art=art)  # 渲染模板


# 删除文章
@app.route('/art/del/<int:id>/', methods=["GET"])
@user_login
def art_del(id):
    art = Art.query.get_or_404(int(id))
    db.session.delete(art)
    db.session.commit()
    return redirect("/art/list/1/")  # 渲染模板


# 文章列表
@app.route('/art/list/<int:page>/', methods=["GET"])
@user_login
def art_list(page=1):
    user = User.query.filter_by(name=session["user"]).first()
    page_data = Art.query.filter_by(user_id=user.id).order_by(Art.addtime.desc()).paginate(page=page, per_page=3)
    cate = [(1, "科技"), (2, "搞笑"), (3, "军事")]
    return render_template("art_list.html", title="文章列表", page_data=page_data, cate=cate)  # 渲染模板


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
