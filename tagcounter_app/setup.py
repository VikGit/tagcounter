from setuptools import setup, find_packages

setup(
    name='tagcounter',
    version='1.0.0',
    description='Tool for counting HTML tags on a web page',
    url='https://github.com/VikGit/Other/blob/master/tagcounter.py',
    author='Viktor Krasheninnikov',
    author_email='krasherspost@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['pycurl', 'argparse', 'bs4', 'tabulate'],
    entry_points={
        'console_scripts': [
            'tagcounter=tagcounter.tagcounter:main'
        ]
    }
)
