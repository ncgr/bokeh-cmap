# cmap2

Reimagining a [cmap](http://soybase.org/cmap/cgi-bin/cmap/viewer?data_source=sbt_cmap;ref_map_set_aid=GmComposite2003&ref_map_aids=GmComposite2003_K&comparative_map_left=GmConsensus40_K;highlight=%22Seed%20oil%201-2%22) style visualization using [Bokeh](http://bokeh.pydata.org/en/latest/) framework.

## Notes

* Download an Anaconda (python3) distribution from  https://www.continuum.io/downloads . miniconda is recommended. After you have the `conda` command, then
* Install dependencies with conda `conda install bokeh pandas `.
* Then Run the builder script on a cmap file:
```
python cmap_builder.py example_data/BAT93_x_JALOEEP558_b.txt 
```
