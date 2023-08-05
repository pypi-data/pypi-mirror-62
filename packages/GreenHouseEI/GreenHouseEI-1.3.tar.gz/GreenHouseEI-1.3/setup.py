import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GreenHouseEI",
    version="1.3",
    author="Zhenghui Su, Yifeng Yu, Yinchao He, Phillip Nguyen, Collin Cornman",
    long_description = long_description,
    long_description_content_type='text/markdown',
    author_email="zsu@huskers.unl.edu",
    description="unzip compressed files that contain plant images, and covert the images into numpy arrays",
    url="https://github.com/collincornman/greenhouseEI",
    license='BSD 2-Clause',
    packages=setuptools.find_packages(),
    zip_safe=True	
 
)
