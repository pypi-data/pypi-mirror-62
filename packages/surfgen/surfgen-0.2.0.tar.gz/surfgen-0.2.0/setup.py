import setuptools
from setuptools import setup
setup(name='surfgen',
version='0.2.0',
description='Tools for creating slab models',
author='Zheng-Da He',
author_email='z.he@fz-juelich.de, jameshzd@mail.ustc.edu.cn, zhengdahe.electrocatalysis@gmail.com',
license='GPL-3.0',
packages=setuptools.find_packages(),
requirements=['ase>=3.19.0', 'pymatgen>=2020.1.28'],
zip_safe=False)
