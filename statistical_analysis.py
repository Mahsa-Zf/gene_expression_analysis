""" 
Module for Statistical Analysis of a Gene Expression Data class instance

This module contains the following classes:
- NoGeneName: A custom error class

- StatisticalAnalysis: Contains methods to statistically analyze the gene expression data.

Usage:
This module can be used to:
- Catch a custom error
- Calculate specific statistical measurements for different genes.
- Find top n genes based on mean differential values
- Find samples with expressions above a threshold value 
  for certain genes and their information such as normal vs. hcc and hcc percentage in
  the found samples

"""

from statistics import mean, stdev, median
import heapq as hq # part of the standard library, implements min heap on top of a regular list
from collections import defaultdict

class NoGeneName(Exception):
    """
    Custom error class for calculate_statistics 
    and calculate_differential methods
    """



class StatisticalAnalysis:

    """
    The StatisticalAnalysis class provides methods for
    performing statistical analyses on gene expression data.

    """

    def __init__(self, gene_exp_inst):

        """
        Initialize the StatisticalAnalysis class with an instance of GeneExpressionData.

        Param 
         - gene_exp_inst: An instance of the GeneExpressionData class.
        """
        self.gene_exp_inst = gene_exp_inst




    def _validate_input(self, gene):
        """
        Private method to make sure that gene names are passed
        """
        if gene not in self.gene_exp_inst.gene_names:
            raise NoGeneName(f"{gene} Doesn't Exist! Enter The Gene Names Correctly.")


    def calculate_statistics(self, *genes):

        """
        Calculate and return the mean, standard deviation, and median for the specified genes.

        Param: 
         - List of gene names.

        Return: 
         - Dictionary with statistical measures for each gene.
           or an error message in case of an invalid gene name
           in the genes list.
        """
        # To avoid gene name repetition
        genes = set(genes)

        gene_stats = defaultdict(dict)
        try:
            # Make sure all the genes in the input are valid
            # before doing any calculations for any of them
            for gene in genes:
                self._validate_input(gene)

            for gene in genes:
                exp_values = [sample_status_value[2] for sample_status_value in\
                               self.gene_exp_inst.gene_expression_values[gene]]
                gene_stats[gene]['mean'] = mean(exp_values)
                gene_stats[gene]['stdev'] = stdev(exp_values)
                gene_stats[gene]['median'] = median(exp_values)

            return gene_stats

        except NoGeneName as e:
            return f'There was an error: {e}'



    def calculate_differential(self, *genes):
        """
        Calculate the differential expression of the specified genes between normal and HCC groups.

        Param: 
         - List of gene names.

        Return: 
         - Dictionary with differential expression for each gene.
           or an error message if there is an invalid gene name in
           the list.
        """
        try:
            # Make sure all the genes in the input are valid
            # before doing any calculations for any of them
            for gene in genes:
                self._validate_input(gene)

            diff_dict = {}
            # Make sure there are no repeated genes in the list
            genes = set(genes)

            for gene in genes:
                # Use _ since the first element is sample name and we're not gonna
                # use it here, but we need it for the for loop
                normal = [value for _, status, value in \
                          self.gene_exp_inst.gene_expression_values[gene] \
                          if status == 'normal']

                hcc = [value for _, status, value in \
                       self.gene_exp_inst.gene_expression_values[gene] \
                       if status == 'HCC']

                # To make sure they are not empty
                if normal and hcc:
                    diff_dict[gene] = mean(hcc) - mean(normal)
                else:
                    diff_dict[gene] = 'Either normal or HCC group is empty'
            return diff_dict

        except NoGeneName as e:
            return f'There was an error: {e}'



    # Additional methods

    # Top n differential genes
    def _gene_generator(self):
        """
        Private method (a generator) to avoid saving all differential values in one place.

        """
        for gene in self.gene_exp_inst.gene_names:
            yield self.calculate_differential(gene)


    def top_n_differential(self, n):
        """
        Find top n genes based on differential values.

        Param:
         - n: number of top genes 

        Return:
         - a list (named heap) containing the sorted values
        """
        heap = []
        gene_diffs = self._gene_generator()

        for gene_diff in gene_diffs:
            # gene_diff is a dictionary with gene name as key
            # and mean difference as value.
            # Here we want to separate the key and value
            # in order to create a tuple and use it for heap operations
            # The indexing [0][0] is because .items() returns a
            # dict_item type object, when casted as list
            # it'll return a list of tuples
            gene_name = list(gene_diff.items())[0][0]
            diff_val = abs(list(gene_diff.items())[0][1])

            if len(heap) < n:
                # After adding the element to the end, heappush bubbles up
                # the element to its correct position in the heap to maintain the heap property

                # By pushing tuples (diff_val, gene_name) onto the heap,
                # you ensure that the heap maintains the ordering by diff_val,
                # because it'll look at the first element for ordering
                # which is crucial for getting the top n elements based on their values.
                hq.heappush(heap, (diff_val, gene_name))

            elif diff_val > heap[0][0]:
                # The new element is inserted in place of the root
                # and then the heap is adjusted to restore the heap property.

                hq.heapreplace(heap, (diff_val, gene_name))

        # Sort the top N genes in descending order of differential values
        return sorted(heap, reverse=True, key=lambda x: x[0])


    # Threshold filtering
    def expression_above_threshold(self, threshold, gene_names):
        """
        Get combinations of genes and samples with expression values above the requested threshold.

        Params:
         - threshold: The expression value threshold.
         - gene_names: Optional specific genes to filter.

        Return: 
        - Dictionary where keys are gene names and values are lists of samples 
          where the expression is above the threshold. Plus sample name and status(hcc/normal)
        """
        # To make sure there are no genes repeated
        gene_names = set(gene_names)

        # If gene names are passed use them, else, we execute the function for all the genes
        if gene_names:

            # validate all the gene names before any calculations
            try:
                # I'm not using *gene_names (*args) parameter
                # Because When you use argparse with nargs='*',
                # it collects the arguments into a list, not a tuple
                # which is the form *args collects the parameters in.
                # When argparse passes the arguments, it doesn't "unpack"
                # the list created by nargs='*'.
                # Instead, it passes this list as a single argument to *gene_names parameter.
                # To handle this, we can avoid using *arg
                # since the nargs=* gives a list to the function.

                for gene_name in gene_names:
                    self._validate_input(gene_name)

                    # create a dictionarie, with each selected gene names and their values
                    genes_to_iterate = {gene_name: self.gene_exp_inst.gene_expression_values[gene_name] \
                                        for gene_name in gene_names}
            except NoGeneName as e:
                return f'There was an error: {e}'

        else:
            # If no gene name is selected, all gene names are used.
            # NOTE THAT IT WILL TAKE TIME TO GATHER ALL 22278 GENES
            genes_to_iterate = self.gene_exp_inst.gene_expression_values

        # Create a dictionary of dictionaries, containing the
        # information about the samples and hcc percentage
        above_threshold = dict()
        for gene, samples in genes_to_iterate.items():
            info, hcc_count, total = defaultdict(list), 0, 0

            for sample, status, value in samples:
                if value > threshold:

                    round_value = round(value, 3)
                    info['info'].append((sample, status, round_value))

                    total += 1
                    if status == 'HCC':
                        hcc_count += 1

            # Make sure total values above threshold is not 0 and handle it if it is
            if total != 0:
                # Set the value of the key (gene) as a dictionary (info)
                above_threshold[gene] = info
                above_threshold[gene]['hcc_percentage'] = round(hcc_count/total*100, 3)
            else:
                above_threshold[gene] = 'No expressions above the threshold.'

        return above_threshold
    