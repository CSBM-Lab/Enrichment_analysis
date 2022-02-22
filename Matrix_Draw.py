'''Based on Perseus v1.6.15.0
Draw a dot plot with enrichment analysis Matrix
'''
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

'''Transform DataFrame x='column name' from string into float, excluding first row'''
def Tf_float(x):
    x = pd.to_numeric(df[x], downcast='float')
    return x

'''Put DataFrame column 'x' into a list, excluding first row'''
def DF_list(x):
    x = df[x][1:].to_list()
    return x

'''Reduce DataFrame based on 'Category column' with value x (GO or KEGG)'''
def DF_Reduce_Cat(x):
    df_filtered = df.loc[df['Category column'] == x]
    return df_filtered

'''Reduce DataFrame based on 'Selection value' with value x (Cluster -number)'''
def DF_Reduce_Select(x):
    df_filtered = df.loc[df['Selection value'] == x]
    return df_filtered

# Read Matrix text file into pandas DataFrame
M_name = 'Matrix_404.txt'
MA_name = 'Matrix_All.txt'
df = pd.read_csv(M_name, sep='\t')
df_all = pd.read_csv(MA_name, sep='\t')

# Reduce DataFrame based on 'Category column' with Cat_input
Cat_input = 'GOMF name' ### Decide which Category to use
df = DF_Reduce_Cat(Cat_input)
# Reduce DataFrame based on 'Selection value' with Sele_input
Select_input = 'Cluster -810' ### Decide which Selection to use '808' or '810'
df = DF_Reduce_Select(Select_input)

# Add a 'Gene Ratio'(Intersection size / Category size) column. !!!First row will be empty (NaN)!!!
df['Intersection size'] = Tf_float('Intersection size')
df['Category size'] = Tf_float('Category size')
df['Gene ratio'] = df['Intersection size'] / df['Category size']
'''This df is ready for plot drawing'''


## Create txt files to check the outcome
df.to_csv('df_GOMF.txt', index=False, sep='\t')
#df_all_reduced.to_csv('df_all_GOBP.txt', index=False, sep='\t')

'''Let's begin to draw the plot'''
# Plot parameters from user
x_input = 'Enrichment factor'
y_input = 'Category value'
c_input = 'Benj. Hoch. FDR'
s_input = 'Intersection size' ### 'Gene ratio' or 'Intersection size'(gene counts) remember to change 'M_size'
Title = ''
x_label = 'Enrichment factor'
y_label = 'Function'

# Transform string into float and modify marker size
M_size = 1 ### 500 for 'Gene ratio', 1 for 'Intersection size'
df[x_input] = Tf_float(x_input)
df[c_input] = Tf_float(c_input)
df[s_input] = M_size * Tf_float(s_input)

# Make data into a list (not necessary for x and y)
x = DF_list(x_input)
y = DF_list(y_input)
c = DF_list(c_input)
s = DF_list(s_input)

print(x)
print(y)
print(c)
print(s)

# setup plot and draw the scatter plot
fig, ax = plt.subplots(figsize=(5, 5)) ### Decide plot size
#axes = plt.gca()
#axes.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.2f}'))
#axes.xaxis.set_major_locator(ticker.MultipleLocator(1))

sc = ax.scatter(x, y, s, c, cmap='coolwarm')

# Set plot margins, Title and labels
ax.margins(0.05, 0.05) ### Decide plot margins
ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
ax.set_title(Title)

# Set up tick locator on x axis
#ax.invert_xaxis()
ax.set_xticks(np.arange(1, 4, 0.5))
#ax.set_xticklabels(['0', '1', '2', '3', '4'])
#ax.xaxis.set_major_locator(ticker.MaxNLocator(5, integer=True))
#ax.invert_xaxis()
#plt.xticks(range(1,3))
#plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1))
#ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.2f}')) 
#ax.xaxis.set_major_locator(ticker.MultipleLocator(2))

# Add a colorbar
cbar = fig.colorbar(sc, anchor=(0, 0), shrink=0.4)
cbar.ax.set_title('FDR', fontdict = {'size':8})

''' Set legend_values from the list 's', 
 divide the list into 5 groups, 
 and grab the last 5 groups' first item '''
# Create a list from 0 to the largest value from the list s
s_list = np.arange(0, int(max(s)), 1).tolist()
legend_values = np.sort(s_list)[::len(s_list)//5][-5:]
#print(legend_values)

# Get the bounds of colorbar axis
xmin, ymin, dx, dy = cbar.ax.get_position().bounds

#print(xmin)
#print(ymin)
#print(dx)
#print(dy)

# Setup new axis for the size chart
xmin -= 0.025
ymin = 0.5
dx = 0.1
dy = dy
sax = fig.add_axes([xmin, ymin, dx, dy], frame_on=False, ymargin=0.15)

# Plot legend size entries onto this axis
x = [0]*len(legend_values)
y = range(len(legend_values))
sizes = legend_values
sax.scatter(x, y, s = sizes, c = 'black', edgecolors = 'none', marker = 'o')

# Decide size chart title
if s_input == 'Intersection size':
    sc_title = 'Gene counts'
elif s_input == 'Gene ratio':
    sc_title = 'Gene ratio'

# Add y axis labels and remove x ticks
sax.yaxis.set_label_position("right")
sax.yaxis.tick_right()
sax.set_yticks(y)
legend_values =  np.round_(legend_values / M_size)
legend_values = legend_values.astype(int) ### Convert the array into integer to remove the '.0'
sax.set_yticklabels(legend_values, fontdict = {'size':8})
sax.set_title(sc_title, loc='left', fontdict = {'size':8})
sax.set_xticks([]) # Set xticks to empty
sax.tick_params(axis='both', which='both', length=0) # Set ticks length to 0 in order to not show

# remove spines
for pos in ['right', 'top', 'bottom', 'left']:
    sax.spines[pos].set_visible(False)


# plt.tight_layout()
plt.savefig('DotPlot_GO.png',bbox_inches='tight')
#plt.show()

### Output filtered data
#df.at[0, 'Gene ratio'] = 'N' # Give Gene ratio Numeric type
