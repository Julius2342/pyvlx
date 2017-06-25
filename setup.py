from setuptools import setup, find_packages

setup(
        name='pyvlx',
        description='PyVLX - controling VELUX windows with Python via KLF 200',

        version='0.1.1',
        download_url='https://github.com/Julius2342/pyvlx/archive/0.1.1.zip',
        url='https://github.com/Julius2342/pyvlx',

        author='Julius Mittenzwei',
        author_email='julius@mittenzwei.com',
        license='LGPL',
        classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Topic :: System :: Hardware :: Hardware Drivers',
          'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
        ],
        packages=find_packages(),
        install_requires=['PyYAML'],
        keywords = 'velux KLF 200 home automation',
        zip_safe=False)
