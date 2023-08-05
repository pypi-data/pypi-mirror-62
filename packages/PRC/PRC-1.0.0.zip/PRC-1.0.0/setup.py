from setuptools import setup

setup(
    name='PRC',
    version='1.0.0',
    author='Damian Nowok',
    author_email='damian.nowok@gmail.com',
    packages=['prc', 'prc.test', 'prc.comm'],
    scripts=['bin/example_prcclient.py','bin/example_prcserver.py'],
    url='http://pypi.python.org/pypi/prc/',
    license='LICENSE.txt',
    description='Python Remote Console',
    long_description=open('README.txt').read(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    install_requires=[
          'future',
      ],
)