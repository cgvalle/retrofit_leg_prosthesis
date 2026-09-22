from setuptools import setup, find_packages
import os


VERSION = os.getenv('VERSION', '1.0.0')

setup(
    name="leg",
    version=VERSION,
    description="EMG-controlled add-on module for a passive transfemoral prosthesis",
    packages=find_packages(include=["leg", "leg.*"]),
    python_requires=">=3.10",
)
