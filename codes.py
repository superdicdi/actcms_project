import os
import random
import uuid

from PIL import Image, ImageDraw, ImageFilter, ImageFont

__author__ = "TuDi"
__date__ = "2018/11/1 下午11:50"


class Code:
    # 随机一个字母或者数字
    def random_chr(self):
        num = random.randint(1, 3)
        if num == 1:
            # 随机生成 0~9 之间的任意数字
            char = random.randint(48, 57)
        elif num == 2:
            # 随机生成 a~z 之间的任意字母
            char = random.randint(97, 122)
        else:
            # 随机生成 A~Z 之间的任意字母
            char = random.randint(65, 90)
        return chr(char)

    # 定义干扰字符颜色
    def random_color1(self):
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 定义字符颜色
    def random_color2(self):
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    def create_code(self):
        width = 240
        height = 60
        image = Image.new("RGB", (width, height), (192, 192, 192))
        # image.show()
        font_name = random.randint(1, 3)
        font_file = os.path.join(os.path.dirname(__file__), "static/fonts") + "/{0}.ttf".format(font_name)
        # font_file = "static/fonts/{0}.ttf".format(font_name)
        font = ImageFont.truetype(font_file, 30)

        # 创建b图片背景上的像素点
        draw = ImageDraw.Draw(image)
        for x in range(0, width, 5):
            for y in range(0, height, 5):
                draw.point((x, y), fill=self.random_color1())

        chars = ""
        # 创建验证码
        for v in range(4):
            c = self.random_chr()
            chars += str(c)
            h = random.randint(5, 15)
            w = width / 4 * v + 10
            draw.text((w, h), c, font=font, fill=self.random_color2())
        # 模糊效果
        image.filter(ImageFilter.BLUR)
        # 将图片保存至本地
        image_name = "{0}.jpg".format(uuid.uuid4().hex)
        # save_dir = "static/code"  # 用相对路径文件夹无法显示，目前不知道原因
        save_dir = os.path.join(os.path.dirname(__file__), "static/code")
        print(os.path.exists(save_dir))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        image.save(save_dir + "/" + image_name, "jpeg")
        return dict(
            img_name=image_name,
            code=chars
        )