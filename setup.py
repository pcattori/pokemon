from setuptools import setup

setup(
    name='pokemon',
    version='0.1.0',
    description='Generation 1 Pokemon lookup and battle simulation',
    url='https://github.com/pcattori/pokemon',
    author='Pedro Cattori',
    author_email='pcattori@gmail.com',
    packages=['pokemon', 'fetch'],
    package_dir={'pokemon': 'pokemon'},
    package_data={'pokemon': ['data/*.json']},
    install_requires=[
        'maps==3.0.1'],
    extras_require={'fetch': [
        'beautifulsoup4==4.5.1',
        'requests==2.12.4']}
)
