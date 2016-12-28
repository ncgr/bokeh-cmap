'''
CMAP loader for local files and remote URLs, supporting CMAP and GFF formats.
'''
import pandas as pd
import os

# headers which (may) exist in a cmap delimited text file
CMAP_HEADERS = [
    'map_acc',
    'map_name',
    'map_start',
    'map_stop',
    'feature_acc',
    'feature_name',
    'feature_aliases',
    'feature_start',
    'feature_stop',
    'feature_type_acc',
    'feature_dbxref_name',
    'feature_dbxref_url',
    'is_landmark',
    'feature_attributes'
]

class Loader():
    def __init__(self, src):
        self.src = src

    def load_dataframe(self):
        '''
        Load src with pandas and confirm the file format is cmap, returning a
        dataframe.
        '''
        df = pd.read_csv(self.src, sep="\t")
        df.src = self.src
        assert self._detect_cmap_dataframe(df), 'cmap file format not detected'
        return df


    def _detect_cmap_dataframe(self, df):
        '''
        Attempt to detect cmap file format by presence of cmap headers in a
        dataframe. If most of the cmap headers are found, call it a match.
        '''
        missing = 0
        for h in CMAP_HEADERS:
            if not h in df:
                missing += 1
        return (missing <= len(CMAP_HEADERS) -1 )

    def _detect_gff_dataframe(self, df):
        '''
        Attempt to detect gff file format by presence of...
        '''
        # TODO: convert GFF into CMAP format dataframe?
        pass
