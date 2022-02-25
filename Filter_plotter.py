'''
Based on Perseus v1.6.15.0
Using enrichment analysis Matrix to filter out a more specific list
then draw a dot plot
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

'''
Reduce [DataFrame] based on 'Category column' with value x 
x = 'GOBP', 'GOCC', 'GOMF' or 'KEGG'
'''
def DF_Reduce_Cat(x):
    df_filtered = df[df['Category column'] == x]
    return df_filtered

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
Transform DataFrame column 'x' into a list
'''
def Tf_list(df,x):
    list = df[x].to_list()
    return list

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

if __name__ == '__main__':
    # Read Matrix text file into pandas DataFrame
    M_file = 'GO_filtered.txt'
    df = pd.read_csv(M_file, sep='\t')

    # Reduce DataFrame based on 'Category column'
    df_GOBP = DF_Reduce_Cat('GOBP')
    df_GOCC = DF_Reduce_Cat('GOCC')
    df_GOMF = DF_Reduce_Cat('GOMF')

    # Reduce DataFrame based on 'Selection value' with Sele_input
    Sele_input = 'Cluster -810' ### Decide which Selection to use ('Cluster -number')
    df_GOBP = DF_Reduce_Sele(df_GOBP,Sele_input)
    df_GOCC = DF_Reduce_Sele(df_GOCC,Sele_input)
    df_GOMF = DF_Reduce_Sele(df_GOMF,Sele_input)

    '''Let's begin to draw the plot'''
    # Plot parameters from [DataFrame] column
    x_input = 'Enrichment factor'
    y_input = 'GO name'
    s_input = 'Intersection size' ### 'Gene ratio' or 'Intersection size'(gene counts) remember to change 'M_size'
    c_input = 'Benj. Hoch. FDR'
    Title = ''
    x_label = 'Enrichment factor'
    y_label = 'Function'

    # Transform string into float and modify marker size
    M_size = 1 ### 500 for 'Gene ratio', 1 for 'Intersection size'
    df_float(df_GOBP)
    df_float(df_GOCC)
    df_float(df_GOMF)
    #df_GOBP.to_csv('df_GOBP.txt', index=False, sep='\t') ### Create a file to check

    # Make data into a list (not necessary for x and y)
    x_GOBP, y_GOBP, s_GOBP, c_GOBP = df_list(df_GOBP)
    x_GOCC, y_GOCC, s_GOCC, c_GOCC = df_list(df_GOCC)
    x_GOMF, y_GOMF, s_GOMF, c_GOMF = df_list(df_GOMF)
    ## print out to check
    #print(x_GOBP)
    #print(y_GOBP)
    #print(s_GOBP)
    #print(c_GOBP)

    # Set norm for colorbar
    c = c_GOBP + c_GOCC + c_GOMF
    c_max = max(c)
    norm = mpl.colors.Normalize(vmin=0, vmax=c_max)

    # get the y count for subplot height_ratios
    h_ratios = [len(y_GOBP), len(y_GOCC), len(y_GOMF)]

    # setup plot and draw the scatter plot
    fig = plt.figure(figsize=(9, 10)) ### Decide plot size (figsize=(5, 5))
    gs = fig.add_gridspec(3, hspace=0, height_ratios=h_ratios) # create 3 rows, hspace is the space between subplots
    axs = gs.subplots(sharex=True, sharey=False)

    axs[0].scatter(x_GOBP, y_GOBP, s_GOBP, c_GOBP, cmap='coolwarm', norm=norm)
    axs[1].scatter(x_GOCC, y_GOCC, s_GOCC, c_GOCC, cmap='coolwarm', norm=norm)
    axs[2].scatter(x_GOMF, y_GOMF, s_GOMF, c_GOMF, cmap='coolwarm', norm=norm)

    ## Set plot margins, Title and labels
    axs[0].margins(0.05, 0.1) ### Decide plot margins
    axs[1].margins(0.05, 0.1) ### Decide plot margins
    axs[2].margins(0.05, 0.5) ### Decide plot margins
    axs[2].set_xlabel(x_label)
    #axs[0].set_ylabel(y_label)
    #ax.set_title(Title)

    # Set up tick locator on x axis
    #ax.invert_xaxis()
    x = x_GOBP + x_GOCC + x_GOMF
    x_min = float(np.floor(min(x))) ### Decide lowest x tick from the min x
    x_max = float(np.ceil(max(x))) ### Decide highest x tick from the max x
    axs[2].set_xticks(np.arange(x_min, x_max+0.5, 0.5))
    # Set another xticks and labels on top of the plot
    axs[0].set_xticks(np.arange(x_min, x_max+0.5, 0.5))
    axs[0].tick_params(top=True)
    axs[0].xaxis.set_tick_params(labeltop=True)
    
    #gs.tight_layout(fig)
    plt.tight_layout() ### Rescale the fig size to fit the data

    # Add a colorbar
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap='coolwarm'),
              ax=axs, anchor=(0, 0), shrink=0.5, orientation='vertical', label='Benj. Hoch. FDR')

    '''
    Set legend_values from the list 's', 
    grabbing the min and max to decide the range of list 
    '''
    s = s_GOBP + s_GOCC + s_GOMF
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
    
    # Get the bounds of colorbar axis
    xmin, ymin, dx, dy = cbar.ax.get_position().bounds

    # Setup new axis for the size chart
    xmin -= 0.02
    ymin = 0.5
    dx = 0.1
    dy -= 0.02
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
    sax.set_yticklabels(legend_values, fontdict = {'size':8})
    sax.set_title(sc_title, loc='left', fontdict = {'size':8})
    sax.set_xticks([]) # Set xticks to empty
    sax.tick_params(axis='both', which='both', length=0) # Set ticks length to 0 in order to not show

    plt.savefig('DotPlot_GO.png')
    #plt.show()