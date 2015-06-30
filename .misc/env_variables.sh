export python_virtualenv=`pyenv prefix`
export python_implementation=`python -c "import platform; print(platform.python_implementation())"`
export python_version=`python -c "import sys; print(str(sys.version_info.major)+'.'+str(sys.version_info.minor))"`
