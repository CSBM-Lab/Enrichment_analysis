# Enrichment_analysis

Enrichment analysis from Perseus v1.6.15.0 output matrix

## Usage

+ prepare 2 matrix files:
- 1 matrix after Hierarchical clustering for data filtering,
- 1 full matrix
+ place file 'go.obo' at ./data/go.obo

## Filter_all.py

Based on Perseus v1.6.15.0
Using Perseus output Matrix to do enrichment analysis, then generate files for plot drawing

### input
- M_file    the matrix after Hierarchical clustering for data filtering
- MA_file   the full matrix

### output
- ./analysis/GO_filtered.txt    the filtered GO terms based on level
- ./analysis/KEGG_filtered.txt  the filtered KEGG names
- ./analysis/Matrix_All_filtered.txt    the matrix with filtered GO terms
- ./analysis/Matrix_sig_filtered.txt    the matrix with only significant and filtered GO terms