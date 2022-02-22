import pandas as pd
from goatools import obo_parser
from io import StringIO
from contextlib import suppress

## Create txt files to check
#df_GO.to_csv('df_GO.txt', index=False)
def Run_filter(col):
    global Row_num, Row_keep
    Row_num = 0 # the row number of GO
    Row_keep = [] # the list of rows to keep
    for i in df_GO[col]:
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
    # Read GO term files as csv into df_GO
    GO_file = 'df_GOMF.txt'
    df_GO = pd.read_csv(GO_file, sep='\t')
    df_GO.dropna(inplace=True) # Drop the rows with (NaN)

    Run_filter('Category value')
    print(Row_keep) ### print the list Row_keep to check
    df_new = df_GO.iloc[Row_keep,:]
    ##print(df_new) ### print the new DataFrame to check
    df_new.to_csv('df_GOMF_filtered.txt', index=False, sep='\t')