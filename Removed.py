import pandas as pd

# Read Matrix text file into pandas DataFrame
M_name = 'Matrix_404.txt'
MA_name = 'Matrix_All.txt'
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
