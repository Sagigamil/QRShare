from setuptools import setup

######################################################################################################
################ You May Remove All the Comments Once You Finish Modifying the Script ################
######################################################################################################

setup(name = 'QRShare', 
      version = '0.1.0',
      description = 'A python package that allow to share files from personl computer to mobile phone easly.',
      py_modules = ["QRShare"],
      package_dir = {'':'src'},
      author = 'AuthorName',
      author_email = 'xyz123@something.com',
      long_description = open('README.md').read() + '\n\n' + open('CHANGELOG.md').read(),
      long_description_content_type = "text/markdown",
      url='https://github.com/jinhangjiang/morethansentiments',
      include_package_data=True,
      classifiers  = [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "License :: OSI Approved :: BSD License",
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Topic :: Text Processing',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
    ],
    install_requires = [
        'qrcode[pil] == 7.3.1',
    ],
    keywords = [],
    entry_points = { 
        'console_scripts': [
            'qrshare=QRShare:main'
        ]
    }
)
