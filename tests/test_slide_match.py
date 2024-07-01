import base64

from src.slide_captcha_match import SlideCaptchaMatch


class TestSlideMatch:

    def __init__(self):
        """
        测试前的初始化操作
        """
        self.background_path = "../data/bg3.jpeg"
        self.slider_path = "../data/slider3.png"
        self.output_path = "../data/output"
        self.processor = SlideCaptchaMatch(save_images=True, output_path=self.output_path)

        # 将图像读取为base64编码
        with open(self.background_path, "rb") as bg_file:
            self.background_base64 = base64.b64encode(bg_file.read()).decode('utf-8')

        with open(self.slider_path, "rb") as slider_file:
            self.slider_base64 = base64.b64encode(slider_file.read()).decode('utf-8')

    def test_get_slider_offset_with_paths(self):
        """
        测试通过路径获取滑块偏移量
        """
        offset = self.processor.get_slider_offset(self.background_path, self.slider_path)
        print(f"Offset (paths): {offset}")

    def test_get_slider_offset_with_base64(self):
        """
        测试通过base64编码获取滑块偏移量
        """
        offset = self.processor.get_slider_offset(self.background_base64, self.slider_base64)
        print(f"Offset (base64): {offset}")


if __name__ == '__main__':
    match = TestSlideMatch()
    # 测试通过路径获取滑块偏移量
    match.test_get_slider_offset_with_paths()
    # 测试通过base64编码获取滑块偏移量
    match.test_get_slider_offset_with_base64()
