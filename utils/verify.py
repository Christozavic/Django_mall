import random
import os
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.http import HttpResponse


class VerifyCode():
    """ 验证码类 """

    def __init__(self, dj_request):
        self.dj_request = dj_request
        self.code_len = 4  # 验证码长度
        self.img_width = 100  # 验证码图片尺寸
        self.img_height = 30  # 验证码图片尺寸

        # django 中 session的名称
        self.session_key = 'verify_code'

    def gen_code(self):
        """ 生成验证码 """
        # 1. 使用随机数生成验证码字符串
        code = self._get_vcode()
        # 2. 把验证码存在 Django 的 session 中
        self.dj_request.session[self.session_key] = code
        # 3. 准备随机元素（背景颜色、验证码文字颜色、干扰线）
        font_color = ['black', 'red', 'blue', 'brown', 'green', 'darkblue', 'darkred']
        # RGB 随机背景色
        bg_color = (random.randrange(230, 255), random.randrange(230, 255), random.randrange(230, 255))
        # 字体路径
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'timesbi.ttf')

        # 创建图片
        im = Image.new('RGB', (self.img_width, self.img_height), bg_color)
        draw = ImageDraw.Draw(im)

        # 画干扰线
        # 随机条数
        for i in range(random.randrange(1, int(self.code_len / 2) + 1)):
            line_color = random.choice(font_color)  # 线条的颜色
            point = (random.randrange(0, self.img_width * 0.2),
                     random.randrange(0, self.img_height),
                     random.randrange(self.img_width - self.img_width * 0.2, self.img_width),
                     random.randrange(0, self.img_height))  # 线条的位置
            width = random.randrange(1, 4)  # 线条的宽度
            draw.line(point, fill=line_color, width=width)

        # 画验证码
        for index, char in enumerate(code):
            code_color = random.choice(font_color)
            font_size = random.randrange(20, 30)
            font = ImageFont.truetype(font_path, font_size)
            point = (index * self.img_width / self.code_len, random.randrange(0, self.img_height / 3))
            draw.text(point, char, font=font, fill=code_color)

        # 把图片写到文件流
        buf = BytesIO()
        im.save(buf, 'gif')
        return HttpResponse(buf.getvalue(), 'image/gif')

    def _get_vcode(self):
        random_str = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789'
        code_list = random.sample(list(random_str), self.code_len)
        code = ''.join(code_list)
        # print(code)
        return code

    def validate_code(self, code):
        """ 验证验证码是否正确 """
        # 1. 转变大小写
        code = str(code).lower()
        vcode = self.dj_request.session.get(self.session_key, '')
        # if vcode.lower() == code:
        #     return True
        # else:
        #     return False
        return vcode.lower() == code


if __name__ == '__main__':
    client = VerifyCode(None)
    client.gen_code()
