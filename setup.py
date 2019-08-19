from setuptools import setup, find_packages


setup(name='oktactl',
      version='0.0.1',
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
            oktactl=oktactl.okta:okta
        ''',
      zip_safe=True,
      include_package_data=True
      )
