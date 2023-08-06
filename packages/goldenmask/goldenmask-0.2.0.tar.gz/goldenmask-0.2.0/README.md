# Goldenmask: Protect your python source code

[简体中文](README_zh_CN.md)

Goldenmask is a tool to protect your python source code easily. It has two methods at the moment: using **Compileall** or using **Cython**. It has a corresponding option named `--layer/-l`, you can choose your favorite method by yourself. Meanwhile, it can protect different file types: python files end with `.py`, wheel packages end with `.whl ` and source package end with `.tar.gz`. 

Goldenmask is a name derived from a  Chinese kungfu named "JinZhongZhao". Because it is not a qualified phrase in a sense,  this name is so unique that can be used as a temporary compilation directory named `__goldenmask__` and a compilation information file named `.goldenmask` which contains the detailed python version string and the platform string.

Let's try to goldenmask now!

## Quick Start

```bash
$ pip install goldenmask
# the default method is Compileall
$ goldenmask yourpythonfile.py
$ tree -a .
.
├── __goldenmask__
│   ├── .goldenmask
│   └── yourpythonfile.pyc
└── yourpythonfile.py

1 directory, 3 files
# repalce your python file
$ goldenmask -i yourpythonfile.py
$ tree -a .
.
├── .goldenmask
└── yourpythonfile.pyc

0 directories, 2 files
# protect python files under directory
$ goldenmask yourpythonmoduledir
# protect the wheel package
$ goldenmask goldenmask-0.1.2-py3-none-any.whl
# protect the source packege
$ goldenmask goldenmask-0.1.2.tar.gz
```

## Installation

Goldenmask is distributed on [PyPI]( https://pypi.org ) and supports Python 3.6+. You can simply install goldenmask as below:

```bash
$ pip install -U goldenmask
```

However, it's a better choice to use a virtual environment:

```bash
$ python -m venv env
# On Windows:
$ .\venv\Scripts\activate
# On Linux:
$ source env/bin/activate
$ pip install goldenmask --upgrade
```

Because goldenmask depends on Cython, you should make sure that there is an appropriate C compiler on your machine. You can see the [detailed guide](https://cython.readthedocs.io/en/latest/src/quickstart/install.html) on Cython's documentation. By the way, if you works on a **Linux** system, you can easily fetch everything you need with one command `sudo apt-get install build-essential` on Ubuntu and `yum groupinstall "Development Tools"` on Centos. However, If you are using **Mac OS X** or **Windows**, you may spend quite some time installing this compilers.

# Usage

You can get everything using [option]() `--help`:

```
$ goldenmask --help
Usage: goldenmask [OPTIONS] [FILES_OR_DIRS]...

  Goldenmask is a tool to protect your python source code easily.

  FILES_OR_DIRS can be python files, wheel packages,source packages or dirs
  contain python files.

Options:
  -l, --layer <int>  Level of protection: 1 - compileall; 2 - cython.
  -i, --inplace      Whether compile python files in place.
  --no_smart         This will copy and compile everything you specified.
  --help             Show this message and exit.
```

## Credits

The [blog](https://prodesire.cn/2019/01/06/%E5%A6%82%E4%BD%95%E5%8A%A0%E5%AF%86%E4%BD%A0%E7%9A%84-Python-%E4%BB%A3%E7%A0%81-%E2%80%94%E2%80%94-%E8%AE%B0-PyCon-China-2018-%E7%9A%84%E4%B8%80%E6%AC%A1%E5%88%86%E4%BA%AB/) from [Prodesire](https://github.com/prodesire).