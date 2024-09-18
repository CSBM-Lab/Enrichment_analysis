'''
Based on Perseus v1.6.15.0
Using Perseus output Matrix for enrichment analysis,
generate a more specific list for plot drawing 
'''
import argparse
import yaml
import pandas as pd
from goatools import obo_parser
from io import StringIO
from contextlib import suppress
from pathlib import Path
from utilities import create_folder, text_color, read_df, df_cat_filter


__author__ = "Johnathan Lin <jagonball@g-mail.nsysu.edu.tw>"
__email__ = "jagonball@g-mail.nsysu.edu.tw"

parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
parser.add_argument("-c","--config_file", required=True, help="config file with necessary parameters.")
args = parser.parse_args()
print(f"The config file used: {text_color(args.config_file, 'bright green')}")


def main():
    ### Load parameters from config file.
    with open(args.config_file, "r") as stream:
        data = yaml.load(stream, Loader=yaml.FullLoader)
    verbose = data["general"]["verbose"]
    project_name = data["general"]["project_name"]
    parent_output_folder = Path(data["general"]["output_folder"])
    output_folder = create_folder(project_name,
                                  parent_output_folder,
                                  verbose=True)
    input_file = Path(data["general"]["input_whole_matrix"])
    df_whole = read_df(input_file)
    input_sig_file = Path(data["general"]["input_sig_matrix"])
    df_sig = read_df(input_sig_file)
    # print(df_sig)
    obo_file = Path(data["general"]["obo_file"])
    
    print(f"Project name: {text_color(project_name, color='bright_yellow')}")
    if verbose:
        print(f"Project name: {text_color(project_name, color='bright_yellow')}")
        print(f"Project folder path: {text_color(output_folder, 'gray')}")
        print(f'The shape of whole matrix: {df_whole.shape}')
        print(f'The shape of significance matrix: {df_sig.shape}')
        print(f"The obo file used: {text_color(obo_file, 'bright_yellow')}")

    # output_folder = Path('C:/Repositories/Enrichment_analysis/analysis/update')
    # # Read Matrix text file into pandas DataFrame
    # M_file = Path('C:/Repositories/Enrichment_analysis/data/Matrix_404.txt')
    # MA_file = Path('C:/Repositories/Enrichment_analysis/data/Matrix_All.txt')
    # significant_name = "Student's T-test Significant D336H_ipc"
    # obo_file = Path('C:/Repositories/Enrichment_analysis/data/go.obo')
    # df = pd.read_csv(M_file, sep='\t')
    # df_all = pd.read_csv(MA_file, sep='\t')
    # df.head()

    ## Reduce dataframe to target category.
    # The annotation category column.
    col_cat = data["go"]["column_category"]
    select_cat = data["go"]["select_category"]
    df_select_cat = df_cat_filter(df_sig, col_cat, select_cat)
    if verbose:
        print(f'The shape of selected category: {df_select_cat.shape}')
    if data["go"]["save_selected_file"]:
        df_select_cat.to_csv(output_folder / data["go"]["selected_file_name"],
                             index=False,
                             sep='\t')
    ### Consider KEGG as selection.
    

    """
    ## Skipping this part for now.
    '''
    Filter with obo_parser, [Level >= 3], then put the rows into the list Row_keep
    then use list_add to add the rows to keep into list_GO for later creating new filtered_DataFrame
    '''
    list_GO = []
    level_filter(df_GOBP, obo_file)
    ## The above level_filter will create 2 lists: Row_keep and Row_drop,
    ## indicating the row numbers to keep or drop.
    print('Rows to keep:', Row_keep) ### print the list Row_keep to check
    list_add(list_GO, df_GOBP)
    ## The above list_add will append the rows to keep as values.
    ## Based on the list Row_keep.

    level_filter(df_GOCC, obo_file)
    print('Rows to keep:', Row_keep) ### print the list Row_keep to check
    list_add(list_GO, df_GOCC)

    level_filter(df_GOMF, obo_file)
    print('Rows to keep:', Row_keep) ### print the list Row_keep to check
    list_add(list_GO, df_GOMF)

    # Create DataFrame from the list, containing all the GO terms filtered, using original df's keys
    df_GO = pd.DataFrame(list_GO, columns=df.keys())
    """


    ## Current DataFrame (df_select_cat) only have GO id, no GO names.
    # Check optional parameters.
    if data["go"]["column_go_level"]:
        level_col = data["go"]["column_go_level"]
    if data["go"]["column_go_depth"]:
        depth_col = data["go"]["column_go_depth"]
    # Annotate GO name (level, depth) based on the GO id.
    print(f"{text_color('Begin parsing GO name from GO ID.', color='bright_yellow')}")
    df_select_cat_name = parse_go_name(df_select_cat,
                                       obo_file,
                                       data["go"]["column_id"],
                                       data["go"]["column_go_name"],
                                       verbose,
                                       level_col,
                                       depth_col,
                                       data["go"]["load_obsolete"],
                                       data["go"]["remove_obsolete"])
    # print(df_select_cat_name)
    if data["go"]["save_go_file"]:
        df_select_cat_name.to_csv(output_folder / data["go"]["go_file_name"],
                                 index=False,
                                 sep='\t')

    ### What the above code do.
    # GO_names = [] # Create a list for GO names
    # GO_name(df_GO, obo_file, GO_names)
    # print(GO_names)
    # df_GO['GO name'] = GO_names # Creating a new column named 'GO name' from the list GO_names
    #
    # df_GO.to_csv(output_folder / 'GO_filtered.txt', index=False, sep='\t') ### Create the file for Filter_plotter.py
    # df_KEGG.to_csv(output_folder / 'KEGG_filtered.txt', index=False, sep='\t') ### Create the file for Filter_plotter.py
    
    # # Create a new list for compare results
    # #df_GO = pd.read_csv(output_folder / 'LL3_GO_filtered.txt', sep='\t') ### skip the above process for testing
    # rows_list = []
    # rows_list = filter_all(df_all, df_GO, 'GOBP', rows_list)
    # rows_list = filter_all(df_all, df_GO, 'GOCC', rows_list)
    # rows_list = filter_all(df_all, df_GO, 'GOMF', rows_list)
    
    # # Create DataFrame from the list
    # df = pd.DataFrame(rows_list, columns=df_all.keys())
    # df = df.sort_index()
    # df = df[~df.index.duplicated(keep='first')] ### Remove duplicates and keep only the first one
    # df.to_csv(output_folder / 'Matrix_All_filtered.txt', index=False, sep='\t') ### Create the file

    # ### Filter the df_whole with target GO ID.
    # # keep the row from df_whole if any GO ID have a match.
    # # Create a "GO_enriched" column with the matched GO terms. (";" separated)
    # ## Performe the above task on each category (GO categories):
    # for i in select_cat:



    # # Create a new list for compare results
    # df_sig = df_all.loc[df_all[significant_name] == '+']
    # rows_list = []
    # rows_list = filter_sig(df_sig, df_all, df_GO, 'GOBP', rows_list)
    # rows_list = filter_sig(df_sig, df_all, df_GO, 'GOCC', rows_list)
    # rows_list = filter_sig(df_sig, df_all, df_GO, 'GOMF', rows_list)

    # # Create DataFrame from the list
    # df = pd.DataFrame(rows_list, columns=df_all.keys())
    # df = df.sort_index()
    # df = df[~df.index.duplicated(keep='first')] ### Remove duplicates and keep only the first one
    # df.to_csv(output_folder / 'Matrix_sig_filtered.txt', index=False, sep='\t') ### Create the file



'''
Use the list Row_keep to add the rows from [DataFrame] to list_GO,
for creating the filtered DataFrame
df = the [DataFrame] related to the list Row_keep
'''
def list_add(list_GO, df):
    for i in Row_keep:
        list_GO.append(df.iloc[i])


'''
Filter [DataFrame] with goatools to filter out more specific targets,
input df = the DataFrame, in which column 'Category value' should be GO terms.
keeping rows which [level = 3]
'''
def level_filter(df, obo_file):
    global Row_num, Row_keep, Row_drop
    Row_num = 0 # the row number of GO
    Row_keep = [] # the list of rows to keep
    Row_drop = [] # the list of rows to drop
    for GO in df['Category value']:
        try:
            GO_levels(GO, obo_file)
            Row_num += 1
        except AttributeError:
            Row_num += 1


def parse_go_name(df, obo_file, col,
                  name_col, verbose,
                  level_col=False,
                  depth_col=False,
                  obsolete=False,
                  remove=False):
    """Parse GO name with goatools, add to a new column.

    :param df: The input DataFrame
    :type df: DataFrame
    :param obo_file: Path to go.obo file
    :type obo_file: str, Path
    :param col: Column name containing GO ID
    :type col: str
    :param name_col: Column name for GO name
    :type name_col: str
    :param level_col: Column name for GO level, defaults to False
    :type level_col: str, optional
    :param depth_col: Column name for GO depth, defaults to False
    :type depth_col: str, optional
    :param obsolete: Show obsolete GO terms, defaults to False
    :type obsolete: bool, optional
    :return: DataFrame with added information
    :rtype: DataFrame
    """
    name_list = []
    level_list = []
    depth_list = []
    obsolete_list = []
    for index, go_id in enumerate(df[col]):
        if verbose:
            term = obo_parser.GODag(obo_file, load_obsolete=obsolete).query_term(go_id)
        else:
            term = obo_parser.GODag(obo_file, load_obsolete=obsolete, prt=None).query_term(go_id)
        # term (GO object): [item_id, level, depth, name, namespace]
        # Some GO id may be obsolete or not found from the provided go.obo file.
        # In these cases the result "term" will be "None".
        if term is not None:
            if verbose:
                print(index, go_id, term.name)
            # print(term)
            # Save the queried name to DataFrame.
            name_list.append(term.name)
            if level_col:
                level_list.append(term.level)
            if depth_col:
                depth_list.append(term.depth)
        else:
            name_list.append("")
            if level_col:
                level_list.append("")
            if depth_col:
                depth_list.append("")
            obsolete_list.append(index)
    df.loc[:, name_col] = name_list
    if level_col:
        df.loc[:, level_col] = level_list
    if depth_col:
        df.loc[:, depth_col] = depth_list
    if remove:
        df.drop(obsolete_list)
    return df


'''
Use obo_parser to filter GO terms, keeping the [level >= 3] Row numbers
GO = GO term to parse
'''
def GO_levels(GO, obo_file):
    term = obo_parser.GODag(obo_file).query_term(GO)
    if term.level >= 3:
        Row_keep.append(Row_num)
        print(GO)
    else:
        Row_drop.append(Row_num)


'''
Compare the filtered selection with the temporary list
'''
def compare_all(df_GO, x,y):
    count = 0
    df = df_GO.loc[df_GO['Category column'] == y]
    for i in df['Category value']:
        if i in x:
            count += 1
            match_GO.append(i)
        else:
            continue
    return count


'''
Select Column based on Cat_input, 
create a list for each row then compare the filtered selection,
keep the matching row
'''
def filter_all(df_all, df_GO, cat, rows_list):
    global match_GO
    for i, v in enumerate(df_all[cat]):
        if type(v) == str:
            list_temp = v.split(';')
            match_GO = [] # Create a list for matched GO
            count = compare_all(df_GO, list_temp, cat)
            if count > 0:
                enriched_GO = ';'.join(match_GO) # transform the list match_GO into a ';' separated string
                # Add a column 'Enriched GO' to the row based on index
                df_all.loc[df_all.index[i], 'Enriched GO'] = enriched_GO
                rows_list.append(df_all.iloc[i])
    return rows_list


'''
Select Column based on Cat_input, 
create a list for each row then compare the filtered selection,
keep the matching row
'''
def filter_sig(df_sig, df_all, df_GO, cat, rows_list):
    global match_GO
    for i, v in enumerate(df_sig[cat]):
        if type(v) == str:
            list_temp = v.split(';')
            match_GO = [] # Create a list for matched GO
            count = compare_all(df_GO, list_temp,cat)

            if count > 0:
                enriched_GO = ';'.join(match_GO) # transform the list match_GO into a ';' separated string
                # Add a column 'Enriched GO' to the row based on index
                df_all.loc[df_all.index[i], 'Enriched GO'] = enriched_GO
                rows_list.append(df_sig.iloc[i])
    return rows_list


if __name__ == '__main__':
    main()
    