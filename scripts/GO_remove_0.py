'''
Based on Perseus v1.6.15.0
Using enrichment analysis Matrix to filter out a more specific list
then draw a dot plot
'''
import pandas as pd

if __name__ == '__main__':
    # Read Matrix text file into pandas DataFrame
    M_file = '../analysis/GO_filtered.txt'
    df = pd.read_csv(M_file, sep='\t')

    '''
    If 'Intersection size' is 0, remove the row

    '''
    df_0 = df[df['Intersection size'] == 0]
    # Remove the selected rows from original DataFrame based on index
    df.drop(index=df_0.index, inplace=True)
    df.to_csv('../analysis/GO_filtered_rm0.txt', index=False, sep='\t') ### Create the file for Filter_plotter.py