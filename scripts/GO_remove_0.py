'''
Based on Perseus v1.6.15.0
Using Perseus output Matrix to do enrichment analysis, generate a more specific list
for plot drawing
'''
import pandas as pd
import sys
import operator
from utilities import read_df, check_type
from pathlib import Path


def main():
    ### TEST ###
    input_func_file = Path("C:/Repositories/Enrichment_analysis/data/Matrix_404.txt")
    input_whole_matrix = Path("C:/Repositories/Enrichment_analysis/data/Matrix_All.txt")
    df_sig = read_df(input_func_file)
    print(df_sig.shape)
    df_whole = read_df(input_whole_matrix)
    print(df_whole.shape)
    target_col = "Intersection size"
    num_cutoff = 0
    symbol = "="
    condition = "keep"

    # df_sig, dict_group_rows_sig = locate_group_rows(df_sig)
    df_whole, dict_group_rows_whole = locate_group_rows(df_whole)
    print(df_whole.head())
    print(dict_group_rows_whole)

    # print(df_sig.dtypes)
    # df_sig[target_col] = df_sig[target_col].astype(float)
    # print(df_sig.dtypes)
    


    # print(operator_dict[symbol])
    # print(operator_dict[symbol](df_sig[target_col], num_cutoff))

    # df_new = df_filter_col_num(df_sig,
    #                            col_name=target_col,
    #                            symbol=symbol,
    #                            num=num_cutoff)
    
    # print(df_new.shape)    


operator_dict = {'>': operator.gt,
                 '<': operator.lt,
                 '=': operator.eq,
                 '>=': operator.ge,
                 '<=': operator.le,
                 '!=': operator.ne}

## Remove rows based on numerical match.
def df_filter_col_num(df,
                      col_name,
                      symbol, # >/</=/>=/<=/!=                  
                      num,
                      connect=None, # and/or
                      col_name2=None,
                      symbol2=None, # >/</=/>=/<=/!=
                      num2=None,
                      condition='keep'):
    # Check inputs: symbol should be str and within operator_dict.keys()
    if not ((type(symbol)==str) and (symbol in operator_dict.keys())):
        print(f"Error, 1")
        sys.exit()
    # Check inputs: num should be (int, float).
    if not check_type(num, (int, float)):
        print(f"Error, 2")
        sys.exit()
    if not connect:  # One condition only.
        if condition=='keep':
            new_df = df[operator_dict[symbol](df[col_name], num)]
        else: # (contition='remove')
            new_df
    else:  # Two conditions
        # Check inputs: connect should be str.
        if not check_type(connect, str):
            print(f"Error, 3")
        # Check the required 2nd inputs.
        if not col_name2 or symbol2 or num2: ## Test if this works.
            print(f"Error, 4")
            sys.exit()
    return new_df


''' 
!!! Perseus output matrix specific function !!!
'''
### May need to check if additional columns are created,
### the reinsert function will have errors or not.
def locate_group_rows(df, marker='#', reinsert=False):
    """Locate the first few rows of information starting with 'marker'.

    :param df: The data matrix.
    :type df: DataFrame
    :param marker: The marker for information rows, defaults to '#'
    :type marker: str, optional
    :param reinsert: To reinsert the rows or not, defaults to True
    :type reinsert: bool, optional
    :return: The removed DataFrame
    :rtype: DataFrame
    :return: A dictionary of removed rows, with index as keys
    :rtype: dict
    """
    rows_group_info = {}
    for index, row in df.iterrows():
        if row.iloc[0].startswith(marker):
            # Row starts with "#"
            rows_group_info[index] = row
        else:  # Break the loop once no '#' is there.
            break
        rows_group_info.keys()
    ### Remove the rows and reset index (drop original index).
    df_mod = df.drop(rows_group_info.keys(), axis=0).reset_index(drop=True)
    
    ##!!! The reinsert can be moved to the end of the program,
    ##!!! or another function before saving output.
    ### Insert the group info rows back to the DataFrame.
    if reinsert:
        # Loop the dictionary to insert row(s).
        for index, row in rows_group_info.items():
            df_mod.iloc[index] = row
    return df_mod, rows_group_info
    

if __name__ == '__main__':
    main()
    
    # # Read Matrix text file into pandas DataFrame
    # M_file = './analysis/GO_filtered_3+_rm.txt'
    # df = pd.read_csv(M_file, sep='\t')

    # '''
    # If 'Intersection size' is 0, remove the row

    # '''
    # df_0 = df[df['Intersection size'] == 0]
    # # Remove the selected rows from original DataFrame based on index
    # df.drop(index=df_0.index, inplace=True)
    # df.to_csv('./analysis/GO_filtered_3+_rm0.txt', index=False, sep='\t') ### Create the file for Filter_plotter.py