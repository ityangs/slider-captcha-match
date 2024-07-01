import base64
import os
from typing import Union, Optional

import cv2
import numpy as np


class SliderCaptchaMatch:
    def __init__(self,
                 gaussian_blur_kernel_size=(5, 5),
                 gaussian_blur_sigma_x=0,
                 canny_threshold1=200,
                 canny_threshold2=450,
                 save_images=False,
                 output_path=""):
        """
        初始化SlideMatch类

        :param gaussian_blur_kernel_size: 高斯模糊核大小，默认(5, 5)
        :param gaussian_blur_sigma_x: 高斯模糊SigmaX，默认0
        :param canny_threshold1: Canny边缘检测阈值1，默认200
        :param canny_threshold2: Canny边缘检测阈值2，默认450
        :param save_images: 是否保存过程图片，默认False
        :param output_path: 生成图片保存路径，默认当前目录
        """
        self.GAUSSIAN_BLUR_KERNEL_SIZE = gaussian_blur_kernel_size
        self.GAUSSIAN_BLUR_SIGMA_X = gaussian_blur_sigma_x
        self.CANNY_THRESHOLD1 = canny_threshold1
        self.CANNY_THRESHOLD2 = canny_threshold2
        self.save_images = save_images
        self.output_path = output_path

    def _remove_alpha_channel(self, image):
        """
        移除图像的alpha通道

        :param image: 输入图像
        :return: 移除alpha通道后的图像
        """
        if image.shape[2] == 4:  # 如果图像有alpha通道
            alpha_channel = image[:, :, 3]
            rgb_channels = image[:, :, :3]

            # 创建一个白色背景
            white_background = np.ones_like(rgb_channels, dtype=np.uint8) * 255

            # 使用alpha混合图像与白色背景
            alpha_factor = alpha_channel[:, :, np.newaxis] / 255.0
            image_no_alpha = rgb_channels * alpha_factor + white_background * (1 - alpha_factor)
            return image_no_alpha.astype(np.uint8)
        else:
            return image

    def _get_gaussian_blur_image(self, image):
        """
        对图像进行高斯模糊处理

        :param image: 输入图像
        :return: 高斯模糊处理后的图像
        """
        return cv2.GaussianBlur(image, self.GAUSSIAN_BLUR_KERNEL_SIZE, self.GAUSSIAN_BLUR_SIGMA_X)

    def _get_canny_image(self, image):
        """
        对图像进行Canny边缘检测

        :param image: 输入图像
        :return: Canny边缘检测后的图像
        """
        return cv2.Canny(image, self.CANNY_THRESHOLD1, self.CANNY_THRESHOLD2)

    def _get_contours(self, image):
        """
        获取图像的轮廓

        :param image: 输入图像
        :return: 轮廓列表
        """
        contours, _ = cv2.findContours(image, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def _get_contour_area_threshold(self, image_width, image_height):
        """
        计算轮廓面积阈值

        :param image_width: 图像宽度
        :param image_height: 图像高度
        :return: 最小和最大轮廓面积阈值
        """
        contour_area_min = (image_width * 0.15) * (image_height * 0.25) * 0.8
        contour_area_max = (image_width * 0.15) * (image_height * 0.25) * 1.2
        return contour_area_min, contour_area_max

    def _get_arc_length_threshold(self, image_width, image_height):
        """
        计算轮廓弧长阈值

        :param image_width: 图像宽度
        :param image_height: 图像高度
        :return: 最小和最大弧长阈值
        """
        arc_length_min = ((image_width * 0.15) + (image_height * 0.25)) * 2 * 0.8
        arc_length_max = ((image_width * 0.15) + (image_height * 0.25)) * 2 * 1.2
        return arc_length_min, arc_length_max

    def _get_offset_threshold(self, image_width):
        """
        计算偏移量阈值

        :param image_width: 图像宽度
        :return: 最小和最大偏移量阈值
        """
        offset_min = 0.2 * image_width
        offset_max = 0.85 * image_width
        return offset_min, offset_max

    def _is_image_file(self, file_path: str) -> bool:
        """
        检查字符串是否是有效的图像文件路径
        """
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
        return os.path.isfile(file_path) and file_path.lower().endswith(valid_extensions)

    def _is_base64(self, s: str) -> bool:
        """
        检查字符串是否是有效的 base64 编码
        """
        try:
            if isinstance(s, str):
                # Strip out data URI scheme if present
                if "data:" in s and ";" in s:
                    s = s.split(",")[1]
                base64.b64decode(s)
                return True
            return False
        except Exception:
            return False

    def _read_image(self, image_source: Union[str, bytes], imread_flag: Optional[int] = None) -> np.ndarray:
        """
        读取图像

        :param image_source: 图像路径或base64编码
        :param imread_flag: cv2.imread 和 cv2.imdecode 的标志参数 (默认: None)
        :return: 读取的图像
        """
        if isinstance(image_source, str):
            if self._is_image_file(image_source):  # 如果是文件路径
                if imread_flag is not None:
                    return cv2.imread(image_source, imread_flag)
                else:
                    return cv2.imread(image_source)
            elif self._is_base64(image_source):  # 如果是 base64 编码
                # Strip out data URI scheme if present
                if "data:" in image_source and ";" in image_source:
                    image_source = image_source.split(",")[1]
                img_data = base64.b64decode(image_source)
                img_array = np.frombuffer(img_data, np.uint8)
                if imread_flag is not None:
                    image = cv2.imdecode(img_array, imread_flag)
                else:
                    image = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)
                if image is None:
                    raise ValueError("Failed to decode base64 image")
                return image
            else:
                raise ValueError("The provided string is neither a valid file path nor a valid base64 string")
        else:
            raise ValueError("image_source must be a file path or base64 encoded string")

    def get_slider_offset(self, background_source: Union[str, bytes], slider_source: Union[str, bytes]) -> int:
        """
        获取滑块的偏移量

        :param background_source: 背景图像路径或base64编码
        :param slider_source: 滑块图像路径或base64编码
        :return: 滑块的偏移量
        """
        background_image = self._read_image(background_source)
        slider_image = self._read_image(slider_source, cv2.IMREAD_UNCHANGED)

        if background_image is None:
            raise ValueError("Failed to read background image")

        if slider_image is None:
            raise ValueError("Failed to read slider image")

        slider_image_no_alpha = self._remove_alpha_channel(slider_image)
        image_height, image_width, _ = background_image.shape

        image_gaussian_blur = self._get_gaussian_blur_image(background_image)
        image_canny = self._get_canny_image(image_gaussian_blur)
        contours = self._get_contours(image_canny)

        if self.save_images:
            # 创建输出目录
            if not os.path.exists(self.output_path):
                os.makedirs(self.output_path)
            cv2.imwrite(f'{self.output_path}/image_canny.png', image_canny)
            cv2.imwrite(f'{self.output_path}/image_gaussian_blur.png', image_gaussian_blur)

        contour_area_min, contour_area_max = self._get_contour_area_threshold(image_width, image_height)
        arc_length_min, arc_length_max = self._get_arc_length_threshold(image_width, image_height)
        offset_min, offset_max = self._get_offset_threshold(image_width)

        offset = None
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if contour_area_min < cv2.contourArea(contour) < contour_area_max and \
                    arc_length_min < cv2.arcLength(contour, True) < arc_length_max and \
                    offset_min < x < offset_max:
                cv2.rectangle(background_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                offset = x

        # 匹配滑块模板在背景中的位置
        result = cv2.matchTemplate(background_image, slider_image_no_alpha, cv2.TM_CCOEFF_NORMED)
        _, _, _, max_loc = cv2.minMaxLoc(result)
        slider_x, slider_y = max_loc
        offset = slider_x

        cv2.rectangle(background_image, (slider_x, slider_y),
                      (slider_x + slider_image_no_alpha.shape[1], slider_y + slider_image_no_alpha.shape[0]),
                      (255, 0, 0), 2)

        if self.save_images:
            cv2.imwrite(f'{self.output_path}/image_label.png', background_image)

        return offset
