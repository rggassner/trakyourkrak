# trakyourkrak
Track your hashcat cracking over time using the machine-readable log viewer  python, pandas, plotly and matplotlib

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

