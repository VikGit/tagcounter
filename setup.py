from setuptools import setup, find_packages

setup(
    name='tagcounter',
    version='1.0.0',
    description='Tool for counting HTML tags on a web page',
    url='https://github.com/VikGit/tagcounter',
    author='Viktor Krasheninnikov',
    author_email='krasherspost@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tagcounter.tests']),
    install_requires=['pycurl', 'pyyaml', 'argparse', 'bs4', 'tabulate'],
    entry_points={
        'console_scripts': [
            'tagcounter=tagcounter.tagcounter:main'
        ]
    }
)
