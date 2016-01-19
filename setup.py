from setuptools import setup

setup(name='template-law-odf',
      version='0.0.1',
      description='Generate ODF documents from jinja2 templated ODT files',
      url='http://github.com/joshgagnon/template-law-odf',
      author='Joshua Gagnon',
      author_email='josh.n.gagnon@gmail.com',
      license='MIT',
     # packages=['template-law-odf'],
      install_requires=[
          'secretary',
      ],
      zip_safe=False)
