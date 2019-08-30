from setuptools import setup, find_packages


setup(name='oktactl',
      version='0.0.8',
      description='Sample Okta CLI tool in python',
      license='MIT',
      author='Atulya Kumar Pandey',
      author_email='atul3015@gmail.com',
      url='https://github.com/atul3015kr/oktactl',
      packages=find_packages(),
      install_requires=[
          'Click',
          'requests'
      ],
      entry_points='''
            [console_scripts]
            oktactl=oktactl.commands:okta
        ''',
      zip_safe=True,
      include_package_data=True,
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      )