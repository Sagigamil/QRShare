# Your First Python Package on PyPI

## [![Typing SVG](https://readme-typing-svg.herokuapp.com?multiline=true&width=1200&lines=An+end+to+end+project+helps+you+publish+your+first+python+package+in+a+simple+way.++++++++++)](https://git.io/typing-svg)

## Step 1

Go to the following two websites to register, respectively.
- PyPI test: https://test.pypi.org/
- PyPI: https://pypi.org/

Note: Let's always try your package on the test site first to avoid mistakes in uploading process. Since any change you make to your package on pypi is not revertable, uploading errors may lead to a malfunctional patch for your package. You want to avoid that!!


## Step 2

Fork this repository to your own GitHub account and make it available in your local. You can make the most changes on GitHub, but you will need to publish your package via cmd with those files available in local.

And here is the list of the core files you will need:

* src
  * __init__.py
  * your_main_code.py  (This is only one module, if you have multi-modules included in this package, you probably want to create subfolders for them)
* setup.py
* README.md
* MANIFEST.in
* LICENSE
* pyproject.toml
* CHANGELOG.md

I know that's a lot. But bear with me. You only need to make necessary changes to some of them and the rest will be stay as default.

## Step 3

Install the following pathon package in your cmd:

    pip install setuptools
    pip install twine
    pip install wheel

You will need them later.

## Step 4

Do the following changes in any order you want:

1. Replace your_main_code.py in src folder with your own python package and leave __init_.py as it is
2. Make changes to setup.py, instructions included in that file.
3. Pick your own license. 
  - Open the LICENSE file, click on Edit, click "Choose a license template", and select the license fullfills your needs.
  - If you have no idea which license works for you, you can use the MIT license, which is one of the most common choices.
  - Or, you can use this link to pick one: https://choosealicense.com/
4. Update CHANGELOG.md to reflect version information
5. Optional: create a test.py and put the file in the tests folder. Or you can remove the whole folder if you are confident that everything works great in your module.