'''
Based on Perseus v1.6.15.0
Using Perseus output Matrix to do enrichment analysis, generate a more specific list
for plot drawing
'''
import pandas as pd

def df_keep_20(df):
        if len(df.index) > 20:
            df.sort_values(by = 'Benj. Hoch. FDR', inplace=True)
            return df.iloc[0:20]
        else:
            return df


if __name__ == '__main__':
    # Read Matrix text file into pandas DataFrame
    M_file = './analysis/GO_filtered_3+_rm0.txt'
    df = pd.read_csv(M_file, sep='\t')

    '''
    Select the 'Category column' and 'Selection value' for sorting and selecting top 20

    '''
    df_GOBP_810 = df[(df['Category column'] == 'GOBP') & (df['Selection value'] == 'Cluster -810')]
    df_GOCC_810 = df[(df['Category column'] == 'GOCC') & (df['Selection value'] == 'Cluster -810')]
    df_GOMF_810 = df[(df['Category column'] == 'GOMF') & (df['Selection value'] == 'Cluster -810')]
    df_GOBP_808 = df[(df['Category column'] == 'GOBP') & (df['Selection value'] == 'Cluster -808')]
    df_GOCC_808 = df[(df['Category column'] == 'GOCC') & (df['Selection value'] == 'Cluster -808')]
    df_GOMF_808 = df[(df['Category column'] == 'GOMF') & (df['Selection value'] == 'Cluster -808')]

    # use df_keep_20 to sort and keep the top 20 based on FDR
    df_GOBP_810 = df_keep_20(df_GOBP_810)
    df_GOCC_810 = df_keep_20(df_GOCC_810)
    df_GOMF_810 = df_keep_20(df_GOMF_810)
    df_GOBP_808 = df_keep_20(df_GOBP_808)
    df_GOCC_808 = df_keep_20(df_GOCC_808)
    df_GOMF_808 = df_keep_20(df_GOMF_808)

    # Merge DataFrame with the new duplicate removed DataFrame
    df_new = pd.concat([df_GOBP_810, df_GOCC_810, df_GOMF_810, df_GOBP_808, df_GOCC_808, df_GOMF_808], ignore_index=False)
    df_new.sort_index(inplace=True) # Sort rows with the original index 
    df_new.to_csv('./analysis/GO_filtered_3+_rm0_top_20.txt', index=False, sep='\t') ### Create the file for Filter_plotter.py