from setuptools import setup

setup(
    name='PJECZ Consultas',
    version='0.2',
    py_modules=['consultas'],
    install_requires=[
        'Click',
        'Jinja2',
        'tabulate',
        ],
    entry_points="""
        [console_scripts]
        consultas=consultas:cli
        """,
)
