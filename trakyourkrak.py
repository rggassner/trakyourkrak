#!/usr/bin/python3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

#Run hashcat with these additional parameters
#Tested with hashcat 6.2.5
#hashcat ...... --machine-readable --outfile report.txt --outfile-format 5,6,1,3,4

#If you have a different file format, set the columns below
absolute_column=0
relative_column=1

#Desired number of time scale labels for matplotlib. Must be larger than 2 and smaller than the number of seconds.
n_time_scale=50
#Group data in this time windows
time_window='1s'
#File to read
log_file='report.txt'

#Comment the line below to use matplotlib
pd.options.plotting.backend = "plotly"

def load_log():
    first = True
    with open(log_file) as infile:
        for line in infile:
            line=line.strip()
            if first:
                steps = []
                times = []
                found = []
                steps.append(int(line.split(":")[absolute_column]))
                first=False
            else:
                if int(line.split(":")[relative_column]) < p_relative_time:
                    steps.append(int(line.split(":")[absolute_column]))
            p_relative_time=int(line.split(":")[relative_column])
            times.append(int(line.split(":")[absolute_column]))
            found.append(1)
    return({'steps':steps,'times':times,'found':found})

def get_steps_df(data):
    #Create data frame, loading data
    df = pd.DataFrame(data['steps'], columns=['steps'])
    #Add a column time converting from epoch to datetime
    df['time'] = pd.to_datetime(df['steps'], unit='s', utc=True).dt.tz_convert(tz="America/Sao_Paulo")
    return df

def get_hc_df(data):
    #Create data frame, loading data
    df = pd.DataFrame(list(zip(data['times'],data['found'])), columns=['epoch','found'])
    #Add a column time converting from epoch to datetime
    df['time'] = pd.to_datetime(df['epoch'], unit='s', utc=True).dt.tz_convert(tz="America/Sao_Paulo")
    #Create a column with cumulative sum os hashes 
    df['found']=df['found'].cumsum()
    #Group by a time window, forward filling values
    df=df.groupby(pd.Grouper(key="time", freq=time_window))['found'].max().ffill()
    return df

def plothc_matplotlib(df,sdf):
    fig, ax = plt.subplots()
    #Create graph
    df.plot.bar(figsize=(17, 7), ylabel='Hash count', xlabel='Time',color='red',title="Hash count over time",ax=ax)
    #Create vertical lines for each step
    fstep=True
    for step in sdf['time']:
        ax.axvline(df.index.searchsorted(step), color="blue", linestyle="--", lw=2, label="Step")
        if fstep:
            ax.legend(['step','hashes'])
            fstep=False  
    #Give the time scale label some space
    fig.subplots_adjust(bottom = 0.22)
    #Set the number of time scale labels
    try:
        myLocator = mticker.MultipleLocator(int(df.count()/(n_time_scale-1)))
    except OverflowError as error:
        myLocator = mticker.MultipleLocator(int(df.count()/2))
    except ValueError as error:
        myLocator = mticker.MultipleLocator(1)
    ax.xaxis.set_major_locator(myLocator)
    #Rotate the time scale labels
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.show()

def plothc_plotly(df,sdf):
    fig = df.plot(title="Number of hashes cracked over time",y='found',
                  labels={"found": "Total hashes cracked"}
                 )
    fig.update_xaxes(rangeslider_visible=True)
    for step in sdf['time']:
        fig.add_vline(x=step, line_width=1, line_dash="dash", line_color="green")
    fig.show()
    
#Read log file
data=load_log()

#Get hashes dataframe
df=get_hc_df(data)

#Get steps dataframe
sdf=get_steps_df(data)

#Plot 
if pd.options.plotting.backend == "plotly":
    plothc_plotly(df,sdf)
else:
    plothc_matplotlib(df,sdf)
