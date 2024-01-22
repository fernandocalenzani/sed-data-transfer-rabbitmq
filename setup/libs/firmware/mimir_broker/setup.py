from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='mimir_broker',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
    author='Arise Technology',
    author_email='projects@arisetechnology.combr',
    description='Broker class using RabbitMQ',
)
