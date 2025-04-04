from setuptools import setup, find_packages

setup(
    name="pomodoro-productivity-suite",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.7.1",
        "Pillow>=9.5.0",
    ],
    entry_points={
        'console_scripts': [
            'pomodoro=main:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive Pomodoro timer with task management and progress tracking",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pomodoro-productivity-suite",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 