# Introduction
GPAS toolbox allows to run various frequently used commands such as pms, master_batcher, pkg_batcher, cnc, praada_nav just by changing values of necessary parameters.
It utilizes python flask in conjunction with jquery.

## Prerequisites
Python flask, and python packages such as pandas. Anaconda comes equipped with various python packages including these. 
So installing Anaconda might be fast way of getting this tool to work.

## Installation
Clone the repository to your local PC.

```
cd <parent dir>
git clone ssh://git@git.blackrock.com/~samrullo/gpas_toolbox_flask.git
cd gpas_toolbox_flask
python __init__.py
```

The above will launch localhost webserver with the port 5000
You can now access the tool by typing ``localhost:5000`` into url