from setuptools import setup, find_packages

setup(
    name='slider-captcha-match',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'opencv-python-headless'
    ],
    entry_points={
        'console_scripts': [
            'slide_match=slide_match.slide_match:SlideMatch',
        ],
    },
    author='ityangs',
    author_email='ityangs@163.com',
    description='A tool for image processing tasks including Gaussian blur and Canny edge detection.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ityangs/slider-captcha-match.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
