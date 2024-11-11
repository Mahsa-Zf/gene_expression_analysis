"""
The main module is responsible the execution of the classs, their methods and creating
a final report based on the commandline arguments

The purpose of using argparse for commandline arguments, is enabling the user
to use *args and add a helper for user convenience.
"""
import argparse
import sys
from gene_expression_data import GeneExpressionData
from statistical_analysis import StatisticalAnalysis
from report import AnalysisReport


def main():
    """
    A main function, containing all the tasks we want to execute
    Return: 
     - Gene names
     - A certain gene's expression value
     - Report of statistical analysis
    """
    # Set up argparse for command-line arguments
    parser = argparse.ArgumentParser(description='Gene Expression Analysis Tool')

    # Arguments for loading the gene expression data
    parser.add_argument('--data_file', type=str, required=True,
                        help='Path to the gene expression data file.')

    # Arguments for getting gene expression values
    parser.add_argument('--gene_name', type=str,
                        help='Gene name for which you want the expression values')
    parser.add_argument('--get_all_gene_names', type=bool,
                        help= "If set True, all gene names are returned")

###################################################################################
    # Arguments for statistical analysis

    # nargs if * allows for zero or more args,
    # if + allows for one or more args, both suited for when we
    # have *args as our function parameter

    # action = extend is useful to allow an option to be specified multiple times.

    parser.add_argument('--statistics', nargs='+', action='extend',
                        help='List of gene names to calculate statistics for.')

    parser.add_argument('--differential', nargs='+', action='extend',
                        help='List of gene names to calculate differential expression for.')

    parser.add_argument('--top_n', type=int,
                        help='Number of top differentially expressed genes to find.')

    parser.add_argument('--threshold', type=float,
                        help='Threshold value to find genes expressed above it.')

    parser.add_argument('--genes_above_threshold', nargs='*', action='extend',
                        help='List of gene names to find values above the threshold (optional).')

###################################################################################

    # Arguments for report generation
    parser.add_argument('--output', nargs='+', action='extend', default=['screen'],
                        help="Output destination(s) for the report (e.g., 'screen', 'output.txt').")

    parser.add_argument(
        '--add', type=str,  nargs='+', action='extend',
        help="Add a new output destination (e.g., 'screen' or a filename)."
    )

    parser.add_argument(
        '--remove', type=str,  nargs='+', action='extend',
        help="Remove an existing output destination (e.g., 'screen' or a filename)."
    )

    # Since __contain__ method takes only 1 item, I don't use narg=+ here
    parser.add_argument(
        '--check', type=str,
        help="Check if a specific destination is in the output destinations list."
    )
###################################################################################

    # Transforms the raw command-line input into a structured, easily accessible format
    args = parser.parse_args()

    # Load gene expression data
    gene_data = GeneExpressionData(args.data_file)

    # This is to catch the FileNotFound error and to terminate the script
    # If there's no error, the attributes gene_names and gene_expression_values are set
    if isinstance(gene_data.load_data(), str):
        sys.exit(gene_data.load_data())

    # Initialize StatisticalAnalysis with the gene expression data instance
    stats_analysis = StatisticalAnalysis(gene_data)

    # Initialize AnalysisReport with the output destinations
    report = AnalysisReport(*args.output)

###################################################################################

    # Add destination
    if args.add:
        report.add_destination(args.add)
        # Using a for loop since args.add is a list of arguments
        for path in args.add:
            print(f"Destination {path} added.")

     # Remove destination
    if args.remove:
        report.remove_destination(args.remove)
        # Using a for loop since arg.remove is a list of arguments
        for path in args.remove:
            print(f"Destination {path} removed.")

    # Check to see if a destination is present in the list of destinations
    if args.check:
        if args.check in report:
            print(f"Destination {args.check} is in the output destinations.")
        else:
            print(f"Destination {args.check} is NOT in the output destinations.")

    # To use __str__ method, and print the final destinations chosen
    print(report)

###################################################################################

    # Get gene names
    if args.get_all_gene_names:
        gene_names = gene_data.get_gene_names()
        report.append_gene_names(gene_names)


    # Get gene expression values
    if args.gene_name:
        gene_exps = gene_data.get_expression_values(args.gene_name)

        # If the gene name doesn't exist, we print the error message
        if isinstance(gene_exps, list):
            report.append_gene_exp(args.gene_name, gene_exps)

        else:
            print(gene_exps)


    # Perform statistical analysis if requested
    if args.statistics:
        genes_stat_info = stats_analysis.calculate_statistics(*args.statistics)

        # If the gene name doesn't exist, the exception handling returns a string
        if isinstance(genes_stat_info, dict):
            report.append_stats(genes_stat_info)     
        else:
            print(genes_stat_info)


    # Perform differential expression analysis if requested
    if args.differential:
        differential = stats_analysis.calculate_differential(*args.differential)

        # If the gene name doesn't exist, the exception handling returns a string
        if isinstance(differential, dict):
            report.append_diff(differential)
        else:
            print(differential)


    # Find top n differentially expressed genes if requested
    if args.top_n:
        top_genes = stats_analysis.top_n_differential(args.top_n)
        report.append_top(args.top_n, top_genes)


    # Find genes expressed above a threshold if requested
    if args.threshold:

        # Get the results
        threshold_results = \
        stats_analysis.expression_above_threshold(args.threshold, args.genes_above_threshold)

        # Check if there was an exception (if yes, it'll return a string)
        if isinstance(threshold_results, dict):
            report.append_thrsh(threshold_results)
        else:
            # if the gene is not found it'll print the returned exception message
            print(threshold_results)


    # Generate the report
    report.output_report()

# Executes main only if the script is directly executed
# Not when it's imported
if __name__ == '__main__':
    main()
