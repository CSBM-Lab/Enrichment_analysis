'''
Based on Perseus v1.6.15.0
Using enrichment analysis Matrix to filter out a more specific list
then draw a dot plot
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from goatools import obo_parser
from io import StringIO
from contextlib import suppress

'''
Transform [NEW DataFrame] x='column name' from string into float, excluding first row
'''
def Tf_float(x):
    x = pd.to_numeric(df[x], downcast='float')
    return x

'''
Reduce [DataFrame] based on 'Category column' with value x (GO or KEGG)
'''
def DF_Reduce_Cat(x):
    df_filtered = df[df['Category column'] == x]
    return df_filtered

'''
Reduce [DataFrame] based on 'Selection value' with value x (cluster-number)
'''
def DF_Reduce_Sele(x):
    df_filtered = df[df['Selection value'] == x]
    return df_filtered

'''
Filter [DataFrame] with goatools to filter out more specific targets,
keeping rows which [depth - level <= 3]
Create a [NEW DataFrame] df
'''
def Run_filter(col):
    global Row_num, Row_keep, Row_drop
    Row_num = 0 # the row number of GO
    Row_keep = [] # the list of rows to keep
    Row_drop = [] # the list of rows to drop
    for i in df[col]:
        with suppress(AttributeError): # Skip the AttributeError(GO term is obsolete, thus not found in GO.obo) and continue
            GO_obo(i)
            Row_num += 1

'''
Use obo_parser to reorganize GO terms
'''
def GO_obo(GO):
    output = StringIO()  ### print value to variable instead of printing to file or monitor
    term = obo_parser.GODag('go.obo').query_term(GO)
    print(term.parents, file=output)  ### redirect the output to variable
    ##print(GO)
    ##print(term.parents)
    data = output.getvalue()  ### get the result of "term" to data, it will change the type of object to string that we can access it
    levels = []
    depths = []
    data = data.split("\n")  ### make each line of output to be a elements of a list
    for go in data:
        go = go.strip()  ### remove the space
        if go.startswith(GO):
            info = go.split("\t")  ### split the parents information to id, level, depth and name
            if len(info) >= 3:  ### filter out the GO term which has no level information (may be root or no child)
                levels.append(int(info[1].replace('level-', "")))
                depths.append(int(info[2].replace('depth-', "")))
    ##print(levels)
    ##print(depths)
    ''' 
    Only keep the rows with depth - levels < 3
    '''
    if levels == []:
        print('empty')
        Row_drop.append(Row_num)
    else:
        count = 0
        for index, item in enumerate(levels):
            ##print(depths[index] - levels[index])
            if depths[index] - levels[index] >=  3:
                count += 1
                print('>=3')
            else:
                print('keep row ' + str(Row_num+1))
        if count == 0: # When count is 0, we keep the row from DataFrame
            Row_keep.append(Row_num)
        else: # When count is not 0, we drop the row from DataFrame
            Row_drop.append(Row_num)

'''
Return GO name of the GO term
'''
def GO_name(GO):
    term = obo_parser.GODag('go.obo').query_term(GO)
    return term.name

'''
Put DataFrame column 'x' into a list
'''
def DF_list(x):
    x = df[x].to_list()
    return x

if __name__ == '__main__':
    # Read Matrix text file into pandas DataFrame
    M_file = 'Matrix_404.txt'
    MA_file = 'Matrix_All.txt'
    df = pd.read_csv(M_file, sep='\t')
    df_all = pd.read_csv(MA_file, sep='\t')

    # Reduce DataFrame based on 'Category column' with Cat_input
    Cat_input = 'GOMF' ### Decide which Category to use
    df = DF_Reduce_Cat(Cat_input)
    # Reduce DataFrame based on 'Selection value' with Sele_input
    Sele_input = 'Cluster -810' ### Decide which Selection to use
    #df = DF_Reduce_Sele(Sele_input)

    ## Reduce df_all to only one column with name Cat_input, excluding first row
    #df_all_reduced = df_all[Cat_input][1:]
    #df_all_reduced.dropna(inplace=True) # Drop the rows with (NaN)

    ## Create 2 txt files to compare
    #df['Category value'].to_csv('df_GOBP.txt', index=False, sep='\t')
    #df_all_reduced.to_csv('df_all_GOMF.txt', index=False, sep='\t')

    #df.dropna(inplace=True) # Drop the rows with (NaN)

    # Filter the data if the Category selected is GO term
    if Cat_input == 'KEGG':
        df = df
    else:
        Run_filter('Category value')
        print('Rows to keep:', Row_keep) ### print the list Row_keep to check
        print('Rows to drop:', Row_drop) ### print the list Row_drop to check
        df.drop(df.index[Row_drop], inplace=True)
        #df = df.iloc[Row_keep,:]
        

        # Replace name with GO term
        for index, GO in enumerate(df['Category value']):
            print(index)
            print(GO)
            print(df.loc[index, 'Category value'])
            df.loc[index, 'Category value'] = GO_name(GO)
            print(df.loc[index, 'Category value'])

    ##print(df) ### print the new DataFrame to check

    # Add a 'Gene Ratio'(Intersection size / Category size) column. !!!First row will be empty (NaN)!!!
    df['Intersection size'] = Tf_float('Intersection size')
    df['Category size'] = Tf_float('Category size')
    df['Gene ratio'] = df['Intersection size'] / df['Category size']
    '''This df is ready for plot drawing'''
    df.to_csv('df_GOMF_filtered.txt', index=False, sep='\t') ### Create a file to check
    
    '''Let's begin to draw the plot'''
    # Plot parameters from [DataFrame] column
    x_input = 'Enrichment factor'
    y_input = 'Category value'
    c_input = 'Benj. Hoch. FDR'
    s_input = 'Intersection size' ### 'Gene ratio' or 'Intersection size'(gene counts) remember to change 'M_size'
    Title = ''
    x_label = 'Enrichment factor'
    y_label = 'Function'

    # Transform string into float and modify marker size
    M_size = 1 ### 500 for 'Gene ratio', 1 for 'Intersection size'
    df[x_input] = Tf_float(x_input)
    df[c_input] = Tf_float(c_input)
    df[s_input] = M_size * Tf_float(s_input)
    df.dropna(inplace=True) # Drop the rows with (NaN)
    ##df.to_csv('df_GOMF_dropped.txt', index=False, sep='\t') ### Create a file to check

    # Make data into a list (not necessary for x and y)
    x = DF_list(x_input)
    y = DF_list(y_input)
    s = DF_list(s_input)
    c = DF_list(c_input)
    print('x:', x)
    print('y:', y)    
    print('s:', s)
    print('c:', c)

    # setup plot and draw the scatter plot
    fig, ax = plt.subplots() ### Decide plot size (figsize=(5, 5))
    sc = ax.scatter(x, y, s, c, cmap='coolwarm')

    # Set plot margins, Title and labels
    ax.margins(0.05, 0.05) ### Decide plot margins
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(Title)

    # Set up tick locator on x axis
    #ax.invert_xaxis()
    x_min = float(np.floor(min(x))) ### Decide lowest x tick from the min x
    x_max = float(np.ceil(max(x))) ### Decide highest x tick from the max x
    ax.set_xticks(np.arange(x_min, x_max+0.5, 0.5))
    #ax.set_xticklabels(['0', '1', '2', '3', '4'])
    #ax.xaxis.set_major_locator(ticker.MaxNLocator(5, integer=True))
    #plt.xticks(range(1,3))
    #plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
    #ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.2f}')) 
    #ax.xaxis.set_major_locator(ticker.MultipleLocator(2))

    # Add a colorbar
    cbar = fig.colorbar(sc, anchor=(0, 0), shrink=0.4)
    cbar.ax.set_title('FDR', fontdict = {'size':8})

    '''
    Set legend_values from the list 's', 
    grabbing the min and max to decide the range of list 
    '''
    ## Create a list from 0 to the largest value from the list s
    #s_list = np.arange(0, int(max(s)), 1).tolist()
    #legend_values = np.sort(s_list)[::len(s_list)//5][-5:]
    # Take the min and max to get the lower and higher values to show
    s_min = int(min(s))
    s_max = int(max(s))
    s_list_min = s_min - (s_min % 10)
    s_list_max = s_max + (10 - (s_max % 10))
    s_list_range = s_list_max - s_list_min
    s_num = 0
    while True:
        if s_num * 20 < s_list_range <= (s_num+1) * 20:
            legend_values = np.arange(s_list_min, s_list_max+11, (s_num+1) * 5).tolist()
            break
        else:
            s_num += 1
    print('legend_values:', legend_values)

    plt.tight_layout() ### Rescale the fig size to fit the data
    # Get the bounds of colorbar axis
    xmin, ymin, dx, dy = cbar.ax.get_position().bounds
    ##print(xmin)
    ##print(ymin)
    ##print(dx)
    ##print(dy)

    # Setup new axis for the size chart
    xmin -= 0.025
    ymin = 0.5
    dx = 0.1
    dy = dy
    sax = fig.add_axes([xmin, ymin, dx, dy], frame_on=False, ymargin=0.15)

    # Plot legend size entries onto this axis
    x = [0]*len(legend_values)
    y = range(len(legend_values))
    sizes = legend_values
    sax.scatter(x, y, s = sizes, c = 'black', edgecolors = 'none', marker = 'o')

    # Decide size chart title
    if s_input == 'Intersection size':
        sc_title = 'Gene counts'
    elif s_input == 'Gene ratio':
        sc_title = 'Gene ratio'

    # Add y axis labels and remove x ticks
    sax.yaxis.set_label_position("right")
    sax.yaxis.tick_right()
    sax.set_yticks(y)
    #legend_values = legend_values.astype(float)
    #legend_values =  np.round_(legend_values / M_size)
    #legend_values = legend_values.astype(int) ### Convert the array into integer to remove the '.0'
    sax.set_yticklabels(legend_values, fontdict = {'size':8})
    sax.set_title(sc_title, loc='left', fontdict = {'size':8})
    sax.set_xticks([]) # Set xticks to empty
    sax.tick_params(axis='both', which='both', length=0) # Set ticks length to 0 in order to not show

    # remove spines
    for pos in ['right', 'top', 'bottom', 'left']:
        sax.spines[pos].set_visible(False)



    plt.savefig('DotPlot_GO.png')
    #plt.show()