#coding=utf-8
from distutils.core import setup
setup(  name='wangSupermath', # 对外我们模块的名字
        version='2.0', # 版本号
        description='这是第一个对外发布的模块，测试哦', #描述
        author='gaoqi', # 作者
        author_email='gaoqi110@163.com',
        py_modules=['wangSupermath.model_A','wangSupermath.model_A2'] # 要发布的模块
 )