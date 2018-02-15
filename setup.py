from setuptools import setup


setup(
    name='Ciclustering',
    description='An automation tool for Collective Idea',
    author='Yuta Katayama',
    author_email='uosotm@gmail.com',
    version='0.1.0',
    py_modules=['ciclustering'],
    install_requires=[
        'click',
        'tqdm',
        'requests',
    ],
    entry_points={'console_scripts': ['ciclustering=main:cli'], },
)
