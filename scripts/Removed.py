import pandas as pd

# Read Matrix text file into pandas DataFrame
M_name = './data/Matrix_404.txt'
MA_name = './data/Matrix_All.txt'
df = pd.read_csv(M_name, sep='\t')
df_all = pd.read_csv(MA_name, sep='\t')

Cat_input = 'GOMF' ### Decide which Category to use

'''Let's compare 'Category value' names back to the original data,
to filter out more specific targets.'''
# Reduce df_all to only one column with name Cat_input, excluding first row
df_all_reduced = df_all[Cat_input][1:]

'''Read through each row, and compare the last 3 items
create a list of matched numbers of rows
'''
Match = [] # Create a list of matched row numbers (first row is 0)
def Comp_df_full():
    global Match
    for i in df_all_reduced:
        if type(i) == str: # Only work on rows with strings
            Temp = [] # Create a list and put each row of selected 'Cat_input' in
            Temp = i.split(';')
            for i, v in enumerate(df['Category value']): # i=index, v=value in this for loop, for each row of v, compare it to the list 'Temp'
                if len(Temp) >= 3: # if the list 'Temp' has at least 3 items, compare v to the last 3
                    if v.casefold() == Temp[-1] or v.casefold() == Temp[-2] or v.casefold() == Temp[-3]:
                        Match.append(i)
                    else:
                        continue
                elif len(Temp) >= 2:# if the list 'Temp' has at least 2 items, compare v to the last 2
                    if v.casefold() == Temp[-1] or v.casefold() == Temp[-2]:
                        Match.append(i)
                    else:
                        continue
                elif len(Temp) >= 1:# if the list 'Temp' has at least 1 items, compare v to the last 1
                    if v.casefold() == Temp[-1]:
                        Match.append(i)
                    else:
                        continue
                else:
                    continue
        else:
            continue
    Match = sorted(set(Match))

Comp_df_full()

'''This is the Matched DataFrame for plot drawing'''
df = df.iloc[Match]


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
    term = obo_parser.GODag('./data/go.obo').query_term(GO)
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
    Filter with obo_parser, [Depths - Levels < 3], then put the rows into the list
    '''
    list_GO = []
    Run_filter(df_GOBP)
    print('Rows to keep:', Row_keep) ### print the list Row_keep to check
    list_add(df_GOBP)

    Run_filter(df_GOCC)
    print('Rows to keep:', Row_keep) ### print the list Row_keep to check
    list_add(df_GOCC)

    Run_filter(df_GOMF)
    print('Rows to keep:', Row_keep) ### print the list Row_keep to check
    list_add(df_GOMF)
    