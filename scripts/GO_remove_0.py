'''
Based on Perseus v1.6.15.0
Using Perseus output Matrix to do enrichment analysis, generate a more specific list
for plot drawing
'''
import pandas as pd

if __name__ == '__main__':
    # Read Matrix text file into pandas DataFrame
    M_file = './analysis/GO_filtered_3+_rm.txt'
    df = pd.read_csv(M_file, sep='\t')

    '''
    If 'Intersection size' is 0, remove the row

    '''
    df_0 = df[df['Intersection size'] == 0]
    # Remove the selected rows from original DataFrame based on index
    df.drop(index=df_0.index, inplace=True)
    df.to_csv('./analysis/GO_filtered_3+_rm0.txt', index=False, sep='\t') ### Create the file for Filter_plotter.py