"""
This module is for the purpose of generating an analysis report.
"""
from datetime import datetime

class AnalysisReport:

    """
    This class is able to output formatted results from analyses to the screen or a file (or both).
    The class should include at least the following functionalities:

    Initialized with the destination(s) of the output (e.g. a filename, or screen).

    Output: a formatted textual report to the destination(s), 
    including nice headers and footers, based on information received through arguments
    in the form of some suitable data type.

    """

    def __init__(self, *output_destinations):

        """
        Initialize the AnalysisReport class with the destination(s) for the output.

        Param: output_destinations: List of destinations such as 'screen', 
        or a filename.
        """

        # The *arg output_destinations is saved as a tuple
        # Should be a list for additional add and remove methods
        self.output_destinations = list(output_destinations)
        self.analysis_results = []
    


    def _write_to_screen(self, content):

        """Private method to output content to the screen."""

        print(content)

    def _write_to_file(self, filename, content):
        """Private method to write content to a file."""
        # Make sure file name has a .txt extension
        if filename[-4:] != '.txt':
            filename = filename+".txt"

        with open(filename, 'a', encoding='utf-8') as file:
            file.write(content + '\n')

    def append_gene_names(self, gene_names):
        """
        Appends a formatted list of gene names to the analysis results.

        Parameters:
            gene_names (list of str): List of gene names to be appended.

        Returns:
            None
        """
        # For display purposes
        gene_names = ', '.join(gene_names)
        self.analysis_results.append({"Gene Names Are": gene_names})

    def append_gene_exp(self, gene_name, gene_exps):
        """
        Appends gene expression values to the analysis results.

        Parameters:
            gene_exps (list of float): List of expression values for a specific gene.

        Returns:
            None
        """
        # For display purposes
        gene_exps = ', '.join(map(str, gene_exps))
        self.analysis_results.append({f"The {gene_name} expression values": f"{gene_exps}"})

    def append_stats(self, genes_stat_info):
        """
        Appends statistical information (mean, standard deviation, and median) 
        for genes to the analysis results.

        Parameters:
            genes_stat_info (dict): A dictionary where keys are gene names and 
                                    values are another dictionary containing
                                    'mean', 'stdev', and 'median'.

        Returns:
            None
        """

        for gene, info in genes_stat_info.items():

        # THE INDENTATION OF FSTRING IS FOR DISPLAY PURPOSES
                self.analysis_results.append({f"Gene Name: {gene}": f"""
Expression Mean: {info['mean']}
Expression Stdev: {info['stdev']}
Expression Median: {info['median']}"""})
                
    def append_diff(self, differential):
        """
        Appends differential expression information for genes to the analysis results.

        Parameters:
            differential (dict): A dictionary where keys are gene names and 
                                values are the difference of means between groups.

        Returns:
            None
        """
        for gene, diff in differential.items():
            self.analysis_results.append({f"Difference of Means for {gene} gene between normal and hcc groups": f"{diff}"})

    def append_top(self, n, top_genes):
        """
        Appends the top N genes with the highest absolute mean differences 
        to the analysis results.

        Parameters:
            n (int): Number of top genes to include.
            top_genes (list of tuples): List of tuples where each tuple contains 
                                        (absolute_mean_difference, gene_name).

        Returns:
            None
        """
        i = 0
        # This is to create a title for this section
        self.analysis_results.append({f'Top {n} Genes': ''})

        for top in top_genes:
            i+=1
            # Remember we had to change the order of gene name
            # and difference value for qheap to work, the order is: (value, name)
            self.analysis_results.append({f"No.{i}) Gene Name: {top[1]}": f"Absolute Mean Difference: {top[0]}"})

    def append_thrsh(self, threshold_results):
        """
        Appends information about genes with expression values above a specified threshold 
        to the analysis results.

        Parameters:
            threshold_results (dict): A dictionary where keys are gene names and values are either:
                                    - A string message indicating no values above the threshold.
                                    - A dictionary containing:
                                        - 'info': A list of tuples (sample, status, value).
                                        - 'hcc_percentage': Percentage of HCC samples above the threshold.

        Returns:
            None
        """
        for gene, info in threshold_results.items():

            # If there are no expressions above threshold
            # we'll have a string as the value for the gene in its dictionary
            if isinstance(info, str):
                self.analysis_results.append({f'For Gene {gene}': f'{info}'})

            else:
                # The next four lines are written for better display of the results
                self.analysis_results.append({f'For Gene {gene}': ''})

                # Iterate through every tuple of (sample, status, value) and create a dict
                # to append to the results list so that we can display each sample's info
                # In a single line.
                for data in info['info']:
                    self.analysis_results.append({f':{data[0]}': f'{data[1]} {data[2]}'})

                self.analysis_results.append({f'HCC Percentage For Gene {gene}': info['hcc_percentage']})

    def output_report(self):
        """
        Output a formatted textual report to the specified destinations.

        """
        # Create formatted report with headers, footers, date and time
        header = "=" * 50 + "\nANALYSIS REPORT\n" + "=" * 50
        timestamp = f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        footer = "=" * 50 + "\nEND OF REPORT\n" + "=" * 50

        body = ""
        if self.analysis_results:
            for analysis in self.analysis_results:
                for key, value in analysis.items():
                    body += f"{key}: {value}\n\n"

            report_content = f"{header}\n{timestamp}\n\n{body}\n{footer}\n\n"

            # Write to all specified destinations
            for destination in self.output_destinations:
                if destination == 'screen':
                    self._write_to_screen(report_content)
                else:
                    self._write_to_file(destination, report_content)
        else:
            self._write_to_screen("No analysis was performed. Please provide arguments to perform an analysis.")

    # Additional Methods
    def __str__(self):
        """
        String representation of the AnalysisReport object.
        Return: String containing the current output destinations.
        """
        destinations = ', '.join(self.output_destinations)
        return f"AnalysisReport configured to output to: {destinations}"


    def __contains__(self, item):
        """
        Allows using the in keyword to check if a particular 
        destination is in the output destinations list.
        Return: Boolean value True if item is among the list
        """
        return item in self.output_destinations


    def add_destination(self, destinations):
        """
        Add a new destination to the output destinations list.
        Param: destination: The new destination to add.
        """
        for destination in destinations:
            if destination not in self.output_destinations:
                self.output_destinations.append(destination)


    def remove_destination(self, destinations):
        """
        Remove a destination from the output destinations list.
        Param: destination: The destination to remove.
        """
        for destination in destinations:
            if destination in self.output_destinations:
                self.output_destinations.remove(destination)
