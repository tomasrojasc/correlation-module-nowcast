## Correlation Module
This module is part of the NOWCAST proyect by [ESO](https://www.eso.org) that aims to do short-term-forecast of the [seeing](https://en.wikipedia.org/wiki/Astronomical_seeing) parameter in order to improve astronomical observations.

## Features
This module makes the discrete cross correlation of two sites' seeing measurements using the module [pydcf](https://github.com/astronomerdamo/pydcf) by Damien Robertson.

## How it works

In order to execute this module, you have to run the file ``main.py``.

The first thing this module does is taking the two files in the folder ``files2cross_corr``. This files have to be named ``file1.csv`` and ``file2.csv`` and they have to have the structure specified in ``files2cross_corr/README.md``. Once those files are in place, it separates the time series in UT time intervals nights, for this it considers a day being from 22ºº hrs to 11ºº of the next day, and the label of the day is given by the first day.

  > Example: Suppose you have the data of 2009-06-03 at 12ºº hrs to 200-06-04 at 14ºº hrs, then a UT day would be from 2009-06-03 22ºº to 200-06-04 11ºº and the ``date_key``associated with this day will be ``2009-06-03``.

Once That is done, it saves each day for each site in a different folder named ``UT_data/file1`` and ``UT_data/file2`` respectively.
Once it has those files, it passes the common dates for the two sites to Damien Robertson's correlation module, and it saves all the outputs to the ``output`` folder.

Then it takes all those outputs that are in csv form and merges them into a pandas dataframe that is saved in the folder ``final_output`` as a binary file.

Finally it makes another binary file containing the maximum correlations and the corresponding shifts, also as a binary file un the ``final_output`` folder.

## How to use
Basically the only thing you have to do is set up ``file1.csv`` and ``file2.csv`` and run the python file ``main.py``

## Things to note
All the intermediate files are deleted after the execution is done. This is to avoid confusions. This can be ignored by deleting the line in ``main.py`` that executes the ``clean.sh`` bash file.

## Credits
  * The pydcf bby Damien Robertson can be found [here](https://github.com/astronomerdamo/pydcf).
