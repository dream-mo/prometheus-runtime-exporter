from setuptools import setup, find_packages

setup(
    name='prometheus-runtime-exporter',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        "psutil",
        "prometheus-client",
    ],
    author='dreammo',
    author_email='dreammovip@163.com',
    description='Python Runtime metrics prometheus exporter',
    license='Apache License',
    keywords='prometheus exporter runtime',
    url='https://github.com/dream-mo/prometheus-runtime-exporter'
)