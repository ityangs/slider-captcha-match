# Slider Captcha Match

## 项目简介

Slider Captcha Match 是一个基于 Python 和 OpenCV 的滑块验证码匹配工具，旨在通过对比滑块和背景图像来计算滑块的正确偏移量。该项目主要用于验证图像处理和匹配算法。

## 目录结构
```bash
.
├── README.md
├── data
│   ├── bg3.jpeg
│   ├── output
│   └── slider3.png
├── pyproject.toml
├── requirements.txt
├── src
│   ├── __init__.py
│   └── slider_captcha_match.py
└── tests
    ├── __pycache__
    └── test_slider_match.py

```

## 安装

1. 克隆仓库到本地：

```bash
git clone https://github.com/ityangs/slider-captcha-match.git
cd slider-captcha-match
```

2. 创建虚拟环境并安装依赖：
```bash
python -m venv venv
source venv/bin/activate  # 在 Windows 上使用 `venv\Scripts\activate`
pip install -r requirements.txt
```

3. 使用 Anaconda 或 Mamba 安装依赖：
```bash
or
mamba create -n slider-captcha-match python=3.10
mamva activate slider-captcha-match
pip install -r requirements.txt

```

## 使用说明

### 核心类 SlideCaptchaMatch

#### 方法1：SlideCaptchaMatch 类包含了进行滑块匹配的核心方法。

```python
from src.slider_captcha_match import SliderCaptchaMatch

processor = SliderCaptchaMatch(save_images=True, output_path="output")

# 通过图像路径获取滑块偏移量
offset = processor.get_slider_offset("data/bg3.jpeg", "data/slider3.png")
print(f"Offset (paths): {offset}")

# 通过 base64 编码获取滑块偏移量
background_base64 = "..."  # base64 编码的背景图像
slider_base64 = "..."  # base64 编码的滑块图像
offset = processor.get_slider_offset(background_base64, slider_base64)
print(f"Offset (base64): {offset}")
```

#### 方法2：

1. 安装依赖：要运行上述代码，需要安装以下 Python 库：

```base
pip install numpy opencv-python slider_captcha_match
```

2. 在安装完所需库后，您可以按照以下步骤使用滑块验证码匹配功能：

- 初始化SliderCaptchaMatch类：配置高斯模糊、Canny边缘检测等参数。
- 读取背景图像和滑块图像：可以是文件路径或base64编码。
- 获取滑块偏移量：调用get_slider_offset函数，返回滑块的准确偏移量。

```python

from slider_captcha_match import SliderCaptchaMatch
from datetime import datetime
import cv2

# 初始化 SliderCaptchaMatch 类
slider_captcha_match = SliderCaptchaMatch(save_images=True, output_path="output")

# 读取背景图像和滑块图像
background_source = "path_to_background_image.jpg"
slider_source = "path_to_slider_image.png"

# 获取滑块偏移量
offset = slider_captcha_match.get_slider_offset(background_source, slider_source)
print(f"滑块偏移量: {offset}")

# 输出结果保存路径
out_file_name = datetime.now().strftime('%Y%m%d%H%M%S.%f')[:-3]
print(f"结果图像保存路径: output/{out_file_name}_image_label.png")

```

### 测试

项目包含基本的测试代码，测试代码位于 tests/test_slide_match.py 中，包含了两种测试方法：
通过路径获取滑块偏移量。
通过 base64 编码获取滑块偏移量。
可以直接运行测试文件来查看效果：

```bash
python tests/test_slider_match.py
```

## 贡献
> 如果你有兴趣为本项目做贡献，请遵循以下步骤：

```bash
1. Fork 本仓库
2. 创建你的 feature 分支 (`git checkout -b feature/fooBar`)
3. 提交你的修改 (`git commit -am 'Add some fooBar'`)
4. 推送到分支 (`git push origin feature/fooBar`)
5. 创建一个新的 Pull Request
```

## 许可证
此项目基于 MIT 许可证，详情请参阅 LICENSE 文件。

## 联系
如果你有任何问题或建议，请通过电子邮件联系我们：ityangs@163.com