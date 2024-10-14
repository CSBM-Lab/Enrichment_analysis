'''
Based on Perseus v1.6.15.0
Using Perseus output Matrix to do enrichment analysis, generate a more specific list
for plot drawing
'''
import pandas as pd
import os
import operator
from utilities import check_type

operator_dict = {'>': operator.gt,
                 '<': operator.lt,
                 '=': operator.eq,
                 '>=': operator.ge,
                 '<=': operator.le,
                 '!=': operator.ne}

## Remove rows based on numerical match.
def df_row_filter_num(df,
                      col_name,
                      symbol, # >/</=/>=/<=/!=                  
                      num,
                      connect=None, # and/or
                      col_name2=None,
                      symbol2=None, # >/</=/>=/<=/!=
                      num2=None,
                      condition='keep'):
    # Check inputs: symbol should be str and within operator_dict.keys()
    if not (type(symbol)==str) and (symbol in operator_dict.keys()):
        print(f"Error")
    # Check inputs: num should be (int, float).
    if not check_type(num, (int, float)):
        print(f"Error")
    if not connect:
        if condition=='keep':
            new_df = df[operator_dict[symbol](df[col_name], num)]
        else: # (contition='remove')
            new_df
    else:
        # Check inputs: connect should be str.
        if not check_type(connect, str):
            print(f"Error")
        # Check the required 2nd inputs.
        if not col_name2 or symbol2 or num2: ## Test if this works.
            print(f"Error")
            os.exit()


if __name__ == '__main__':
    
    
    
    
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