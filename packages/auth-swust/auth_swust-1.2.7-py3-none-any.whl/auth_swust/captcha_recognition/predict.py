import string

import torch
from PIL import Image
from pathlib import Path

from .img_process import process
from .lenet5 import LeNet5
from .segment import segment_image

# 使用绝对路径 设置model的位置
model_path = str(Path(__file__).parent.joinpath('model', 'captcha_cnn.pth'))

state_dict = torch.load(model_path)
net = LeNet5()
net.eval()
net.load_state_dict(state_dict)

label_list = string.digits + string.ascii_uppercase


def decode(index):
    return label_list[index]


def predict(subimages):
    t = []
    all = None
    s = ""
    for i, x in enumerate(subimages, 0):
        t.append(
            torch.from_numpy(subimages[i]).view(-1, 1, 32,
                                                32).to(torch.float32))
        if i == 3:
            all = torch.cat(t)
    for x in range(4):
        s += decode(net(all)[x].argmax())
    return s


def predict_captcha(captcha_image: Image.Image):
    """
    :param captcha_image: captcha image path
    :return: str 验证码
    """
    # segment_iamge 抽取小图像，降噪指数默认 2
    image = process(captcha_image)
    subimages = segment_image(image)

    # 第一遍没抽取出来四张，再来第二遍
    if subimages is None:
        # segment_iamge 抽取小图像  降噪指数 3
        image = process(captcha_image, 3)
        subimages = segment_image(image)

    if subimages is not None:
        return predict(subimages)

    # 如果切割图片返回 None 说明没有切割出来 直接不预测
    return None
