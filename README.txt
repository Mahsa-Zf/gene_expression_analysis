PROJECT TITLE
================================================
Gene Expression Analysis Project

================================================

DESCRIPTION
================================================

This project is built to facilitate the analysis of liver cancer gene expression data by performing 
a series of statistical computations. The code is modular, consisting of several classes that handle
specific tasks such as loading data, calculating statistical values, and generating reports.

The key components are:

* GeneExpressionData Class: Handles reading liver cancer gene expression data and storing it in an easily accessible format.

* StatisticalAnalysis Class: Performs statistical analyses on the gene expression data, including calculating means, standard deviations, and other differential values.

* AnalysisReport Class: Generates formatted reports to display the statistical analysis results, either on the screen or in a file.

================================================

GETTING STARTED
================================================
Dependencies >>>>>>>>>>>>

* Python 3.x

Libraries:
* statistics (standard Python library)
* collections (standard Python library)
* argparse (standard Python library)
* heapq (standard Python library)

Ensure that your Python environment is set up with the necessary modules before running the program. 

Installing >>>>>>>>>>>>

* Clone this repository to your local machine: git clone <https://github.com/Mahsa-Zf/gene_expression_analysis>
* Navigate to the cloned directory


Executing program >>>>>>>>>>>>

* Make sure all the required .py files (gene_expression_data.py, statistical_analysis.py, report.py, and main.py) are in the same directory.
* Run the main script using Python
* Replace data/liver_cancer_gene_expression.csv with the path to your input data file. 
* Example of commandline execution
```
python main.py --data_file data/liver_cancer_gene_expression.csv --top_n 5 --threshold 10

```
AVAILABLE PARAMETERS: 

* --data_file: Path to the CSV file containing liver cancer gene expression data.
* --gene_name: Gene name for which you want the expression values.
* --get_all_gene_names: If set True, all gene names are returned.
* --statistics: List of gene names to calculate statistics for.
* --differential: List of gene names to calculate differential expression for.
* --top_n: Number of top differentially expressed genes to analyze.
* --threshold: Threshold value for filtering gene expression.
* --genes_above_threshold: List of gene names to find values above the threshold (optional).
* --output: Output destination(s) for the report (e.g., 'screen', 'output.txt').
* --add: Add a new output destination.
* --remove: Remove an existing output destination.
* --check: Check if a specific destination is in the output destinations list.

================================================
HELP
================================================

In case you need help regarding command-line arguments, you can use the following command to view available options:
```
python main.py --help

```
================================================
AUTHOR
================================================

Mahsa Zamanifard


