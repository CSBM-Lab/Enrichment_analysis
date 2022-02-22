'''Based on Perseus v1.6.15.0
Using enrichment analysis Matrix to filter out a more specific list
'''
import pandas as pd
import numpy as np
from goatools import obo_parser
from io import StringIO
from contextlib import suppress

'''Transform [NEW DataFrame] x='column name' from string into float, excluding first row'''
def Tf_float(x):
    x = pd.to_numeric(df_new[x], downcast='float')
    return x

'''Reduce [DataFrame] based on 'Category column' with value x (GO or KEGG)'''
def DF_Reduce_Cat(x):
    df_filtered = df.loc[df['Category column'] == x]
    return df_filtered

'''Reduce [DataFrame] based on 'Selection value' with value x (cluster-number)'''
def DF_Reduce_Sele(x):
    df_filtered = df.loc[df['Selection value'] == x]
    return df_filtered

'''Filter [DataFrame] with goatools to filter out more specific targets,
keeping rows which [depth - level <= 3]
Create a [NEW DataFrame] df_new
'''
def Run_filter(col):
    global Row_num, Row_keep
    Row_num = 0 # the row number of GO
    Row_keep = [] # the list of rows to keep
    for i in df[col]:
        with suppress(AttributeError): # Skip the AttributeError(GO term is obsolete, thus not found in GO.obo) and continue
            GO_obo(i)
            Row_num += 1

# Use obo_parser to reorganize GO terms
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
    ''' Only keep the rows with depth - levels < 3'''
    if levels == []:
        print('empty')
    else:
        count = 0
        for index, item in enumerate(levels):
            ##print(depths[index] - levels[index])
            if depths[index] - levels[index] >= 3:
                count += 1
                print('>=3')
            else:
                print('keep row ' + str(Row_num+1))
        if count == 0: # When count is 0, we keep the row from DataFrame
            Row_keep.append(Row_num)


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
    #Sele_input = 'Cluster-810' ### Decide which Selection to use
    #df = DF_Reduce_Sele(Sele_input)

    ## Reduce df_all to only one column with name Cat_input, excluding first row
    #df_all_reduced = df_all[Cat_input][1:]
    #df_all_reduced.dropna(inplace=True) # Drop the rows with (NaN)

    ## Create 2 txt files to compare
    #df['Category value'].to_csv('df_GOBP.txt', index=False, sep='\t')
    #df_all_reduced.to_csv('df_all_GOMF.txt', index=False, sep='\t')

    df.dropna(inplace=True) # Drop the rows with (NaN)

    Run_filter('Category value')
    print(Row_keep) ### print the list Row_keep to check
    df_new = df.iloc[Row_keep,:]
    ##print(df_new) ### print the new DataFrame to check
    
    ## Add a 'Gene Ratio'(Intersection size / Category size) column. !!!First row will be empty (NaN)!!!
    #df_new.loc['Intersection size'] = Tf_float('Intersection size')
    #df_new.loc['Category size'] = Tf_float('Category size')
    #df_new['Gene ratio'] = df_new.loc['Intersection size'] / df_new.loc['Category size']
    '''This df is ready for plot drawing'''
    ##df_new.to_csv('df_GOMF_filtered.txt', index=False, sep='\t') ### Create a file to check
    
