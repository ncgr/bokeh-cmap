# bokeh-cmap

prototype of a [cmap](http://soybase.org/cmap/cgi-bin/cmap/viewer?data_source=sbt_cmap;ref_map_set_aid=GmComposite2003&ref_map_aids=GmComposite2003_K&comparative_map_left=GmConsensus40_K;highlight=%22Seed%20oil%201-2%22) style visualization using [Bokeh](http://bokeh.pydata.org/en/latest/) framework.


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
Now you should see in your browser:


