# Array_Utilities
Useful scripts for manipulating SAC data for an array:

  - Baz_Trace_Remover.py - move traces depending on the backazimuth thay arrive at the stations with.

  - Ep_Trace_Remover.py - move traces depending on the epicentral distance of the station they were recorded at.

  - Replace_Data_Synthetic.py - replaces data with a ricker wave at the predicted phase arrival time in each trace.
  
Requires:
  - obspy
  - numpy
  - scipy
  - argparse
  - shutil
  - glob
  
