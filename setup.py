from setuptools import setup

def globdata():
    from glob import glob
    import os.path
    dir = os.path.join(os.path.dirname(__file__), 'pyfortune')
    for file in glob(os.path.join(dir, 'data', '*')):
        if not os.path.splitext(file)[1] and os.path.isfile(file):
            yield file.replace(dir, '').lstrip('/\\')
    for file in glob(os.path.join(dir, 'data', 'off', '*')):
        if not os.path.splitext(file)[1] and os.path.isfile(file):
            yield file.replace(dir, '').lstrip('/\\')

setup(
    name = 'PyFortune',
    version = '0.1',
    packages = ['pyfortune'],
    package_data = {
        'pyfortune': list(globdata()),
    },
    entry_points = {
        'console_scripts': [
            'fortune = pyfortune.entry:main',
            'pyfortune = pyfortune.entry:main'
        ]
    },

    # metadata for upload to PyPI
    author = 'xiaomao',
    author_email = 'xiaomao5@live.com',
    url = 'https://github.com/xiaomao5/pyfortune',
    description = 'Port of the classic fortune program to python',
    keywords = 'fortune port unix game',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Games/Entertainment',
        'Topic :: Utilities',
    ],
)
