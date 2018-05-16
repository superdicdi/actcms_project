from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)


# 登录
@app.route('/login/', methods=["GET", "POST"])
def login():
    return render_template("login.html", title="登录")  # 渲染模板


# 注册
@app.route('/register/', methods=["GET", "POST"])
def register():
    return render_template("register.html", title="注册")  # 渲染模板


# 登出
@app.route('/logout/', methods=["GET"])
def logout():
    return redirect("/login/")  # 重定向到登录页面


# 发布文章
@app.route('/art/add/', methods=["GET", "POST"])
def art_add():
    return render_template("art_add.html")  # 渲染模板


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
    return render_template("art_list.html")  # 渲染模板


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)
