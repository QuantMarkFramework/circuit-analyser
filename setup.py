from setuptools import find_packages, setup


def read_requirements(filename):
	with open(filename) as file:
		return [r.strip() for r in file.readlines()]


setup(
	name='analyser',
	packages=find_packages(),
	version='0.1.0',
	description='A python library for analysing quantum circuits.',
	license='MIT',
	install_requires=read_requirements('requirements.txt'),
	test_require=read_requirements('dev_requirements.txt')
)
