# Introduction
GPAS toolbox allows to generate various frequently used commands such as pms, master_batcher, pkg_batcher, cnc, praada_nav by specifiying necessary parameters.
It utilizes python flask in conjunction with jquery and can be runs as local webserver.

## Prerequisites
Python flask, and python packages such as pandas are required. [Anaconda](https://www.anaconda.com/download/) comes equipped with various python packages including these. 
Installing Anaconda might be fast way of getting this tool to work.

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

## Simple Usage

This is how top page looks like. Press on the pms,cnc,pkg_batcher link.
![Alt text](docs/screenshots/top.JPG?raw=True "Top page")

Next following screen will show up
![Alt text](docs/screenshots/second_page.JPG?raw=True "Top page")

Press PMS link. It will open PMS command generator page. After the page loads press F5 to refresh the page, to make jquery functions available.
![Alt text](docs/screenshots/pms_template.JPG?raw=True "Top page")

Fill in CLIENT, Package, Fund, Date parameters and Directory parameter will automatically refer to usual report folder of that client e.g. /d0/prod1/reports/gp_reports/MAIN/20181212
At this point when you press "Generic pms" button, pms scratch command with all specified parameter values in place will show up with switches highlighted in green and the command itself highlighted in red.
![Alt text](docs/screenshots/pms_template_generic.JPG?raw=True "Top page")
