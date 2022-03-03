'''
Based on Perseus v1.6.15.0
Using enrichment analysis Matrix to filter out a more specific list
then draw a dot plot
'''
import pandas as pd

if __name__ == '__main__':
    # Read Matrix text file into pandas DataFrame
    M_file = '../analysis/GO_filtered_rm0.txt'
    df = pd.read_csv(M_file, sep='\t')

    '''
    Select the 'Category column' and 'Selection value' for removing duplicates,

    '''
    Cat_col = 'GOBP'
    Sele_val = 'Cluster -810'
    df_du = df[(df['Category column'] == Cat_col) & (df['Selection value'] == Sele_val)]
    # Remove the selected rows from original DataFrame based on index
    df.drop(index=df_du.index, inplace=True)

    # Remove duplicates based on 'GO name', sort by FDR then keep the lowest FDR duplicate
    df_du.sort_values(by = 'Benj. Hoch. FDR', inplace=True)
    df_du.drop_duplicates(subset='GO name', keep='first', inplace=True)

    # Merge DataFrame with the new duplicate removed DataFrame
    df_new = pd.concat([df, df_du], ignore_index=False)
    df_new.sort_index(inplace=True) # Sort rows with the original index 
    df_new.to_csv('../analysis/GO_filtered_rm.txt', index=False, sep='\t') ### Create the file for Filter_plotter.py