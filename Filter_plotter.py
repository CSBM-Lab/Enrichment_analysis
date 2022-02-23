'''
Based on Perseus v1.6.15.0
Using enrichment analysis Matrix to filter out a more specific list
then draw a dot plot
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
Reduce [DataFrame] based on 'Category column' with value x (GO or KEGG)
'''
def DF_Reduce_Cat(x):
    df_filtered = df[df['Category column'] == x]
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
    df_float(df_GOBP)
    df_float(df_GOCC)
    df_float(df_GOMF)
    #df_GOBP.to_csv('df_GOBP.txt', index=False, sep='\t') ### Create a file to check

    # Make data into a list (not necessary for x and y)
    x_GOBP, y_GOBP, s_GOBP, c_GOBP = df_list(df_GOBP)
    x_GOCC, y_GOCC, s_GOCC, c_GOCC = df_list(df_GOCC)
    x_GOBP, y_GOBP, s_GOBP, c_GOBP = df_list(df_GOMF)
    ## print out to check
    #print(x_GOBP)
    #print(y_GOBP)
    #print(s_GOBP)
    #print(c_GOBP)

    # setup plot and draw the scatter plot
    fig, ax1 = plt.subplots() ### Decide plot size (figsize=(5, 5))
    sc = ax1.scatter(x, y, s, c, cmap='coolwarm')

    # Set plot margins, Title and labels
    ax.margins(0.05, 0.05) ### Decide plot margins
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(Title)
