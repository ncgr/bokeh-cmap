# bokeh-cmap

prototype of a cmap style visualization using [Bokeh](http://bokeh.pydata.org/en/latest/) framework.


:warning: this is a very quick script cobbled together while learning bokeh. Things that definitely need to be done:

* use pandas instead of petl for loading csv
* break up the script into manageable python modules
* accept command line options for other data files
* etc !

## Notes

1. Download Anaconda (python3) distribution from  https://www.continuum.io/downloads . miniconda is recommended. After you have the `conda` command, then
2. Install dependencies:
```
conda install bokeh petl
```
3. Edit `demo.py` so the SOURCES list points to two cmap format data files.
3. Start bokeh server. This is required because this demo has some interactivity implemented in python.
```
bokeh serve
```
4. Run the script
```
 python demo.py
```
