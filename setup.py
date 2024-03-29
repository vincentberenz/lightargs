from setuptools import setup, find_packages

setup( name='lightargs',
       version='1.26',
       description='simple arguments manager for python',
       classifiers=[
           'License :: OSI Approved :: MIT License',
           'Programming Language :: Python :: 2.7',
           'Programming Language :: Python :: 3',
       ],
       keywords='arguments parser',
       url='https://github.com/vincentberenz/lightargs.git',
       author='Vincent Berenz',
       author_email='vberenz@tuebingen.mpg.de',
       license='MIT',
       packages=['lightargs'],
       install_requires=['argcomplete',"colorama"],
       zip_safe=True
)



