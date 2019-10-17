# This purpose of this script is to provide a means to hash the ids
# This is purely for data setup purposes.

import hashlib
import sys
from biom import load_table
from biom.util import biom_open
import pandas as pd

table_fname = sys.argv[1]
taxa_fname = sys.argv[2]
table = load_table(table_fname)
taxa = pd.read_csv(taxa_fname, sep='\t')

fid_map = {id_: hashlib.md5(id_.encode('utf-8')).hexdigest()
           for id_ in table.ids(axis='observation')}
table.update_ids(fid_map, axis='observation', inplace=True)

with biom_open(table_fname + '.sum', 'w') as f:
    table.to_hdf5(f, 'md5')

taxa['featureid'] = taxa.featureid.apply(lambda id_: hashlib.md5(id_.encode('utf-8')).hexdigest())
taxa = taxa.set_index('featureid')
taxa.to_csv(taxa_fname + '.sum', sep='\t')
