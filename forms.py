from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from models import User

__author__ = "TuDi"
__date__ = "2018/5/12 上午12:10"


class LoginForm(FlaskForm):
    """
    登录表单：账号、密码
    """
    name = StringField(
        label="账号",
        validators=[
            DataRequired("账号不能为空")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号",
            "required": False,
        }
    )
    password = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码",
            "required": False,
        }
    )
    submit = SubmitField(
        label="登录",
        render_kw={
            "class": "btn btn-primary",

        }
    )
    def validate_name(self, field):

        name = field.data
        user = User.query.filter_by(name=name).count()
        if not user > 0:
            raise ValidationError("当前用户未注册")

    def validate_password(self, field):
        pwd = field.data
        user = User.query.filter_by(name=self.name.data).first()
        if user:
            if not user.check_pwd(pwd):
                raise ValidationError("密码不正确")


class RegisterForm(FlaskForm):
    """
    注册表单：账号、密码、确认密码、验证码、注册按钮
    """
    name = StringField(
        label="账号",
        validators=[
            DataRequired("账号不能为空")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号"
        }
    )
    password = PasswordField(
        label="密码",
        validators=[
            DataRequired("密码不能为空")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码"
        }
    )
    repassword = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("确认密码不能为空"),
            EqualTo('password', message="密码输入不一致")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入确认密码"
        }
    )

    code = StringField(
        label="验证码",
        validators=[
            DataRequired("验证码不能为空")
        ],
        description="验证码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入验证码"
        }
    )

    submit = SubmitField(
        label="注册",
        render_kw={
            "class": "btn btn-success",
        }
    )

    # 自定义验证规则，validate_字段名
    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user > 0:
            raise ValidationError("账号已存在！")

    # 自定义验证规则，validate_字段名
    def validate_code(self, field):
        code = field.data
        if "code" not in session:
            raise ValidationError("验证码出错，请刷新页面")
        if code.lower() != session["code"].lower():
            raise ValidationError("验证码不正确")


class PublishArtForm(FlaskForm):
    """
    发布文章表单：标题、分类、封面、内容、发布文章按钮
    """
    title = StringField(
        label="标题",
        validators=[
            DataRequired("标题不能为空")
        ],
        description="标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入标题"
        }
    )

    category = SelectField(
        label="分类",
        validators=[
            DataRequired("分类不能为空")
        ],
        description="分类",
        choices=[(1, "科技"), (2, "搞笑"), (3, "军事")],
        default=1,
        coerce=int,
        render_kw={
            "class": "form-group",
        }
    )

    logo = FileField(
        label="封面",
        validators=[
            DataRequired("封面不能为空")
        ],
        description="封面",
        render_kw={
            "class": "form-control-file",
        }
    )

    content = TextAreaField(
        label="内容",
        validators=[
            DataRequired("内容不能为空")
        ],
        description="内容",
        render_kw={
            "id": "content",
            "style": "height: 300px"
        }
    )
    submit = SubmitField(
        label="发布文章",
        render_kw={
            "class": "btn btn-primary",
        }
    )


class EditArtForm(FlaskForm):
    """
    修改章表单：当前修改文章的id，标题、分类、封面、内容、确认修改按钮
    """

    id = IntegerField(
        label="id",
        validators=[
             DataRequired("id不能为空")
         ],
    )
    title = StringField(
        label="标题",
        validators=[
            DataRequired("标题不能为空")
        ],
        description="标题",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入标题",
            "required": False
        }
    )

    category = SelectField(
        label="分类",
        validators=[
            DataRequired("分类不能为空")
        ],
        description="分类",
        choices=[(1, "科技"), (2, "搞笑"), (3, "军事")],
        default=1,
        coerce=int,
        render_kw={
            "class": "form-group",
            "required": False
        }
    )

    logo = FileField(
        label="封面",
        validators=[
            DataRequired("封面不能为空")
        ],
        description="封面",
        render_kw={
            "class": "form-control-file",
            "required": False
        }
    )

    content = TextAreaField(
        label="内容",
        validators=[
            DataRequired("内容不能为空")
        ],
        description="内容",
        render_kw={
            "id": "content",
            "style": "height: 300px"
        }
    )
    submit = SubmitField(
        label="确认修改",
        render_kw={
            "class": "btn btn-primary",
        }
    )