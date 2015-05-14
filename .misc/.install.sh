if python --version | grep 3\.4 ; then
  pip install coveralls codecov munkres3
fi

sudo apt-get install espeak libclang1-3.4
sudo ln -s /usr/lib/x86_64-linux-gnu/libclang.so.1 /usr/lib/x86_64-linux-gnu/libclang.so
