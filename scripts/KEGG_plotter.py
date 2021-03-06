'''
Based on Perseus v1.6.15.0
Using Perseus output Matrix to do enrichment analysis, generate a more specific list
for plot drawing
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

'''
Reduce [DataFrame] based on 'Selection value' with value x
df = the DataFrame, x = 'Cluster -number'
'''
def DF_Reduce_Sele(df,x):
    df_filtered = df[df['Selection value'] == x]
    return df_filtered

'''
Transform [NEW DataFrame] x='column name' from string into float
df = the DataFrame, x = the column name
'''
def Tf_float(df,x):
    float = pd.to_numeric(df[x], downcast='float')
    return float

'''
Transform x, c, s into float with Tf_float
df = the DataFrame
'''
def df_float(df):
        df[x_input] = Tf_float(df,x_input)
        df[c_input] = Tf_float(df,c_input)
        df[s_input] = M_size * Tf_float(df,s_input)
        df.dropna(inplace=True) # Drop the rows with (NaN)

'''
Transform x, y, c, s into list for plot drawing
df = the DataFrame
'''
def df_list(df):
    x = Tf_list(df,x_input)
    y = Tf_list(df,y_input)
    s = Tf_list(df,s_input)
    c = Tf_list(df,c_input)
    ## print out to check
    print('x:', x)
    print('y:', y)    
    print('s:', s)
    print('c:', c)
    return x,y,s,c

'''
Transform DataFrame column 'x' into a list
'''
def Tf_list(df,x):
    list = df[x].to_list()
    return list

if __name__ == '__main__':
    # Read Matrix text file into pandas DataFrame
    M_file = './analysis/KEGG_filtered_rm0.txt'
    df = pd.read_csv(M_file, sep='\t')

    # Reduce DataFrame based on 'Selection value' with Sele_input
    Sele_input = 'Cluster -808' ### Decide which Selection to use ('Cluster -number')
    df_Cluster_1 = DF_Reduce_Sele(df,Sele_input)
    Sele_input = 'Cluster -810' ### Decide which Selection to use ('Cluster -number')
    df_Cluster_2 = DF_Reduce_Sele(df,Sele_input)

    '''Let's begin to draw the plot'''
    # Plot parameters from [DataFrame] column
    x_input = 'Enrichment factor'
    y_input = 'Category value'
    s_input = 'Intersection size' ### 'Gene ratio' or 'Intersection size'(gene counts) remember to change 'M_size'
    c_input = 'Benj. Hoch. FDR'
    Title = ''
    x_label = 'Enrichment factor'
    y_label = 'Function'

    # Transform string into float and modify marker size
    M_size = 1 ### 500 for 'Gene ratio', 1 for 'Intersection size'
    df_float(df_Cluster_1)
    df_float(df_Cluster_2)
    #df_Cluster_1.to_csv('./analysis/df_KEGG_plot.txt', index=False, sep='\t') ### Create a file to check

    # Make data into a list (not necessary for x and y)
    x_Cluster_1, y_Cluster_1, s_Cluster_1, c_Cluster_1 = df_list(df_Cluster_1)
    x_Cluster_2, y_Cluster_2, s_Cluster_2, c_Cluster_2 = df_list(df_Cluster_2)
    ## print out to check
    #print(x_Cluster_1)
    #print(y_Cluster_1)

    # Set norm for colorbar
    c = c_Cluster_1 + c_Cluster_2
    c_max = max(c)
    norm = mpl.colors.Normalize(vmin=0, vmax=c_max)

    # get the y count for subplot height_ratios
    h_ratios = [len(y_Cluster_1), len(y_Cluster_2)]

    
    # setup plot and draw the scatter plot
    fig = plt.figure(figsize=(7, 3.3)) ### Decide plot size (figsize=(5, 5))
    gs = fig.add_gridspec(2, hspace=0, height_ratios=h_ratios) # create 3 rows, hspace is the space between subplots
    axs = gs.subplots(sharex=True, sharey=False)

    axs[0].scatter(x_Cluster_1, y_Cluster_1, s_Cluster_1, c_Cluster_1, cmap='coolwarm', norm=norm)
    axs[1].scatter(x_Cluster_2, y_Cluster_2, s_Cluster_2, c_Cluster_2, cmap='coolwarm', norm=norm)

    ## Set plot margins, Title and labels
    axs[0].margins(0.05, 0.2) ### Decide plot margins
    axs[1].margins(0.05, 0.08) ### Decide plot margins
    axs[1].set_xlabel(x_label, fontdict = {'size':12})
    #axs[0].set_ylabel(y_label)
    #ax.set_title(Title)

    # Set up tick locator on x axis
    #ax.invert_xaxis()
    x = x_Cluster_1 + x_Cluster_2
    x_min = float(np.floor(min(x))) ### Decide lowest x tick from the min x
    x_max = float(np.ceil(max(x))) ### Decide highest x tick from the max x
    axs[1].set_xticks(np.arange(x_min, x_max+0.5, 0.5))
    # Set another xticks and labels on top of the plot
    axs[0].set_xticks(np.arange(x_min, x_max+0.5, 0.5))
    axs[0].tick_params(top=True)
    axs[0].xaxis.set_tick_params(labeltop=True)
    plt.tight_layout() ### Rescale the fig size to fit the data

    # Add a colorbar
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap='coolwarm'),
              ax=axs, anchor=(0, 0), shrink=0.5, orientation='vertical', label='Benj. Hoch. FDR')

    '''
    Set legend_values from the list 's', 
    grabbing the min and max to decide the range of list 
    '''
    s = s_Cluster_1 + s_Cluster_2
    s_min = int(min(s))
    s_max = int(max(s))
    s_list_min = s_min - (s_min % 10)
    s_list_max = s_max + (10 - (s_max % 10))
    s_list_range = s_list_max - s_list_min
    s_num = 0
    while True:
        if s_num * 30 < s_list_range <= (s_num+1) * 30:
            legend_values = np.arange(s_list_min, s_list_max+11, (s_num+1) * 5).tolist()
            break
        else:
            s_num += 1
    legend_values = [i for i in legend_values if i != 0] # remove '0' from the list
    print('legend_values:', legend_values)
    
    '''
    Get the bounds of colorbar axis
    xmin = x location, ymin = y location, dx = x length, dy = y length
    '''
    xmin, ymin, dx, dy = cbar.ax.get_position().bounds

    # Setup new axis for the size chart
    xmin -= 0.01
    ymin = 0.55
    dx = 0.05
    dy = dy
    sax = fig.add_axes([xmin, ymin, dx, dy], frame_on=False, ymargin=0.15)

    # Plot legend size entries onto this axis
    x = [0]*len(legend_values)
    y = range(len(legend_values))
    sizes = legend_values
    sax.scatter(x, y, s = sizes, c = 'black', edgecolors = 'none', marker = 'o')
    sc_title = 'Gene counts'

    # Add y axis labels and remove x ticks
    sax.yaxis.set_label_position("right")
    sax.yaxis.tick_right()
    sax.set_yticks(y)
    legend_values = [item / M_size for item in legend_values]
    legend_values = [round(num,0) for num in legend_values]
    legend_values = [int(item) for item in legend_values] ### Convert the list into integer to remove the '.0'
    sax.set_yticklabels(legend_values)
    sax.set_ylabel(sc_title)
    sax.set_xticks([]) # Set xticks to empty
    sax.tick_params(axis='both', which='both', length=0) # Set ticks length to 0 in order to not show

    plt.savefig('./analysis/DotPlot_KEGG.png')
    #plt.show()