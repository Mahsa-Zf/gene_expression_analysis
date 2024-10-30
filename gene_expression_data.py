""" 
Module for Gene Expression Data

This module contains the following class:
- GeneExpressionData: Represents and manipulates liver cancer gene expression data.

Usage:
This module can be used to load gene expression data, get gene names and their expression values.

"""
from collections import defaultdict


class GeneExpressionData:
    """
    The GeneExpressionData Class will do the following:

    - Initialize the class with a file path to liver cancer gene expression data.
    - Read and load the gene expression data from the file into a suitable data structure.
    - Return a list of gene names from the data.
    - Given a gene name, return its expression values across different samples.

    """

    def __init__(self, file_path):
        """
        Initialize the GeneExpressionData class with a file path to the data file.

        """
        self.file_path = file_path

        # Two attributes to load the information in
        self.gene_expression_values = defaultdict(list)
        self.gene_names = []

    def load_data(self):
        """
        Load gene expression data from the file into memory.
        This method is run in the main script, to make sure
        there's no error when reading the file.

        Output: 
         - Error message and exiting the script if the file's not found
         - Loading the data into gene_expression_values and gene_names if there's no error
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file_handle:
                # Read header line to get gene names
                header = file_handle.readline().strip().split(',')

                # Skip the first two elements to get to gene names
                self.gene_names = header[2:]

                # Extract gene expression data
                for line in file_handle:
                    line_parts = line.strip().split(',')
                    sample, status, *expression_values = line_parts

                    # Use map to directly create an iterator, reducing memory usage
                    expression_values = map(float, expression_values)

                    # Save each gene's expression values with its status and sample name for
                    # Using in the differential statistical analysis
                    for gene_name, value in zip(self.gene_names, expression_values):
                        self.gene_expression_values[gene_name].append((sample, status, value))

        except FileNotFoundError as e:
            return f"Error! {e}"


    def get_gene_names(self):
        """
        Returns a list of gene names from the data.

        Could just use the attribute as well but
        Created a method since it specifically said return
        The gene
        """
        return self.gene_names

    def get_expression_values(self, gene_name):
        """
        Given a gene name, return its expression values across different samples.

        Param: 
         - gene_name: The name of the gene.

        Return: 
         - a list containing expression values.
        """
        if gene_name not in self.gene_names:
            # Since this error can be caught easily
            # I didn't write a custom error class for it
            return f"Gene {gene_name} not found in data."
        # Use list comprehension to get only the values and not the status and sample name
        return [sample_status_value[2] for sample_status_value\
                 in self.gene_expression_values[gene_name]]
    