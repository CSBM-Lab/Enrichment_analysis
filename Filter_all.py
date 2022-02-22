'''
Based on Perseus v1.6.15.0
Using enrichment analysis Matrix to filter out a more specific list
then draw a dot plot
'''
import pandas as pd
import numpy as np
from goatools import obo_parser
from io import StringIO
from contextlib import suppress

from sklearn.decomposition import KernelPCA

'''
Reduce [DataFrame] based on 'Category column' with value x (GO or KEGG)
'''
def DF_Reduce_Cat(x):
    df_filtered = df[df['Category column'] == x]
    return df_filtered

'''
Filter [DataFrame] with goatools to filter out more specific targets,
input df = the DataFrame, in which column 'Category value' should be GO terms.
keeping rows which [depth - level <= 3]
'''
def Run_filter(df):
    global Row_num, Row_keep, Row_drop
    Row_num = 0 # the row number of GO
    Row_keep = [] # the list of rows to keep
    Row_drop = [] # the list of rows to drop
    for i in df['Category value']:
        with suppress(AttributeError): # Skip the AttributeError(GO term is obsolete, thus not found in GO.obo) and continue
            GO_obo(i)
            Row_num += 1

'''
Use obo_parser to reorganize GO terms
input GO = GO term.
'''
def GO_obo(GO):
    output = StringIO()  ### print value to variable instead of printing to file or monitor
    term = obo_parser.GODag('go.obo').query_term(GO)
    print(term.parents, file=output)  ### redirect the output to variable
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
    ''' 
    Only keep the rows with depth - levels < 3
    '''
    if levels == []: # When the lists of levels and depths are empty
        print('empty')
        Row_drop.append(Row_num) # Add the Row number to the list Row_drop
    else: # When the lists of levels and depths are not empty
        count = 0
        for index, value in enumerate(levels): # go through each set of leves and depths
            ##print(depths[index] - levels[index])
            if depths[index] - levels[index] >= 3: # if this number >= 3 means we don't want
                count += 1 # count +1 for adding it to drop list
                print('>=3')
            else: # other rows are the ones to keep
                print('keep row ' + str(Row_num+1)) # showing which rows to keep
        if count == 0: # When count is 0, we keep the row from DataFrame
            Row_keep.append(Row_num)
        else: # When count is not 0, we drop the row from DataFrame
            Row_drop.append(Row_num)

'''
Use the list Row_keep to add the rows from [DataFrame] to list_GO,
for creating the filtered DataFrame
df = the [DataFrame] related to the list Row_keep
'''
def list_add(df):
    for i in Row_keep:
        list_GO.append(df.iloc[i])

'''
Filter [DataFrame] with goatools to filter out more specific targets,
input df = the DataFrame, in which column 'Category value' should be GO terms.
keeping rows which [level >= 3]
'''
def level_filter(df):
    global Row_num, Row_keep, Row_drop
    Row_num = 0 # the row number of GO
    Row_keep = [] # the list of rows to keep
    Row_drop = [] # the list of rows to drop
    for i in df['Category value']:
        with suppress(AttributeError): # Skip the AttributeError(GO term is obsolete, thus not found in GO.obo) and continue
            GO_levels(i)
            Row_num += 1

'''
Use obo_parser to filter GO terms with [level]
GO = GO term to parse
'''
def GO_levels(GO):
    term = obo_parser.GODag('go.obo').query_term(GO)
    if term.level == 4:
        Row_keep.append(Row_num) 
    else:
        Row_drop.append(Row_num)

'''
Compare the filtered selection with the temporary list
'''
def compare_all(x,y):
    count = 0
    df = df_GO.loc[df_GO['Category column'] == y]
    for i in df['Category value']:
        if i in x:
            count += 1
        else:
            continue
    return count

'''
Select Column based on Cat_input, 
create a list for each row then compare the filtered selection,
keep the matching row
'''
def filter_all(cat):
    for i, v in enumerate(df_all[cat]):
        if type(v) == str:
            list_temp = v.split(';')
            count = compare_all(list_temp,cat)
            if count > 0:
                the_list.append(df_all.loc[i])
            else:
                continue
        else:
            continue

if __name__ == '__main__':
    # Read Matrix text file into pandas DataFrame
    M_file = 'Matrix_404.txt'
    MA_file = 'Matrix_All.txt'
    df = pd.read_csv(M_file, sep='\t')
    df_all = pd.read_csv(MA_file, sep='\t')

    '''
    Filter GO term with obo_parser
    '''
    Cat_input = 'GOBP' ### Decide which Category to use
    df_GOBP = DF_Reduce_Cat(Cat_input)
    Cat_input = 'GOCC' ### Decide which Category to use
    df_GOCC = DF_Reduce_Cat(Cat_input)
    Cat_input = 'GOMF' ### Decide which Category to use
    df_GOMF = DF_Reduce_Cat(Cat_input)

    '''
    Filter with obo_parser, [Depths - Levels < 3], then put the rows into the list
    '''
    #list_GO = []
    #Run_filter(df_GOBP)
    #print('Rows to keep:', Row_keep) ### print the list Row_keep to check
    #list_add(df_GOBP)
#
    #Run_filter(df_GOCC)
    #print('Rows to keep:', Row_keep) ### print the list Row_keep to check
    #list_add(df_GOCC)
#
    #Run_filter(df_GOMF)
    #print('Rows to keep:', Row_keep) ### print the list Row_keep to check
    #list_add(df_GOMF)
    
    '''
    Filter with obo_parser, [Levels = 3], then put the rows into the list
    '''
    list_GO = []
    level_filter(df_GOBP)
    print('Rows to keep:', Row_keep) ### print the list Row_keep to check
    list_add(df_GOBP)

    level_filter(df_GOCC)
    print('Rows to keep:', Row_keep) ### print the list Row_keep to check
    list_add(df_GOCC)

    level_filter(df_GOMF)
    print('Rows to keep:', Row_keep) ### print the list Row_keep to check
    list_add(df_GOMF)


    # Create DataFrame from the list, containing all the GO terms filtered
    df_GO = pd.DataFrame(list_GO, columns=df.keys())
    df_GO.to_csv('GO_filtered.txt', index=False, sep='\t') ### Create the file to check
    ##df_GO = pd.read_csv('GO_filtered.txt', sep='\t') ### skip the above process for testing
    # Create a new list for compare results
    the_list = []
    filter_all('GOBP')
    filter_all('GOCC')
    filter_all('GOMF')
    
    # Create DataFrame from the list
    df = pd.DataFrame(the_list, columns=df_all.keys())
    df = df.sort_index()
    df = df[~df.index.duplicated(keep='first')]
    df.to_csv('Matrix_All_filtered.txt', index=False, sep='\t') ### Create the file