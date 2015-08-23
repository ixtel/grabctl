from setuptools import setup, find_packages
import os

ROOT = os.path.dirname(os.path.realpath(__file__))

setup(
    name='grabctl',
    version='0.0.1',
    description='UI and daemon to control Grab spiders',
    long_description=open(os.path.join(ROOT, 'README.rst')).read(),
    url='http://github.com/lorien/grabctl',
    author='Gregory Petukhov',
    author_email='lorien@lorien.name',

    packages=find_packages(exclude=['test']),
    install_requires=['six', 'psutil'],
    scripts = ['bin/grabctl'],

    license="MIT",
    keywords="grab crawler spider scraping daemon panel",
    classifiers=(
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ),
)
