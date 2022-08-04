# trakyourkrak
Track your hashcat cracking over time using this graphical log viewer. Used python, pandas, plotly and matplotlib. Tested with hashcat 6.2.5, since machine-readable is quite recent you might need to update.

Both tools allow pan and zoom. Vertical lines represent a reset in relative time (mask changing for example). You can switch tools by commenting the line:
```
pd.options.plotting.backend = "plotly"
```

Plotly using '1s' time_window
![plotly](/images/plotly.png)

Matplotlib using '5min' time_window. Vertical lines overlaps, meaning that at least one reset happened within that time frame.
![matplotlib](/images/matplotlib.png)


Add the following parameters to your hashcat session. 
```
--machine-readable --outfile report.txt --outfile-format 5,6,1,3,4
```

Only fields 5 and 6 are used for visualization. If you have already generated a report with another format, you can configure columns with these variables:
```
absolute_column=0
relative_column=1
```

According to hashcat manual 
```
- [ Outfile Formats ] -

  # | Format
 ===+========
  1 | hash[:salt]
  2 | plain
  3 | hex_plain
  4 | crack_pos
  5 | timestamp absolute
  6 | timestamp relative
```

