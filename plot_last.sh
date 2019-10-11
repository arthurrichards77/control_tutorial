last_log=$(ls logs | tail -1)
python fgplot.py logs/$last_log
