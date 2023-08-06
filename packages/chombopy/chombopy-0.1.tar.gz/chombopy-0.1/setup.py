from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='chombopy',
      version='0.1',
      description='Running, analysing and plotting Chombo simulations',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/jrgparkinson/mushy-layer',
      author='Jamie Parkinson',
      author_email='jamie.parkinson@gmail.com',
      license='MIT',
      packages=find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      zip_safe=False)