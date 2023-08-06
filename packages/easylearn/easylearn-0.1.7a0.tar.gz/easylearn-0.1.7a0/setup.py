#-*- coding:utf-8 -*-

"""
Created on 2020/02/29
------
@author: LI Chao
Email: lichao19870617@gmail.com or lichao19870617@163.com
"""

from setuptools import setup, find_packages


setup(
    name='easylearn',
    version='0.1.7.alpha',
    description=(
        'This project is designed for machine learning in resting-state fMRI field'
    ),
    long_description='Please see the README',
    author='Chao Li',
    author_email='lichao19870617@gmail.com',
    maintainer='Chao Li +',
    maintainer_email='lichao19870617@gmail.com',
    license='MIT License',
    packages=find_packages(),
    platforms=["all"],
    url='https://github.com/lichao312214129/lc_rsfmri_tools_python',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'joblib==0.14.1',
        'numpy==1.18.1',
        'pandas==1.0.1',
        'python-dateutil==2.8.1',
        'pytz==2019.3',
        'scikit-learn==0.22.2',
        'scipy==1.4.1',
        'six==1.14.0',
        'nibabel==3.0.1',
        'imbalanced-learn==0.6.2',
        'skrebate==0.6',
        'matplotlib',
        ],
)