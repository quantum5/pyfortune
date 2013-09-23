from setuptools import setup, find_packages
setup(
    name = "PyFortune",
    version = "0.1",
    packages = ['pyfortune'],
    package_data = {
        'pyfortune': ['data/*'],
    },
    entry_points = {
        'setuptools.installation': [
            'eggsecutable = pyfortune.entry:main',
        ],
        'console_scripts': [
            'fortune = pyfortune.entry:main',
            'pyfortune = pyfortune.entry:main'
        ]
    },

    # metadata for upload to PyPI
    author = "xiaomao",
    author_email = "me@example.com",
    description = "Attempted port of the classic fortune program to python",
    license = "GPL",
    keywords = "fortune port unix",
)
