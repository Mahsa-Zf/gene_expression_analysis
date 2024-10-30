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

    def output_report(self, analysis_data):
        """
        Output a formatted textual report to the specified destinations.
        param: analysis_data: A dictionary or other suitable data structure
        containing report information.
        """
        # Create formatted report with headers, footers, date and time
        header = "=" * 50 + "\nANALYSIS REPORT\n" + "=" * 50
        timestamp = f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        footer = "=" * 50 + "\nEND OF REPORT\n" + "=" * 50

        body = ""
        for analysis in analysis_data:
            for key, value in analysis.items():
                body += f"{key}: {value}\n\n"

        report_content = f"{header}\n{timestamp}\n\n{body}\n{footer}\n\n"

        # Write to all specified destinations
        for destination in self.output_destinations:
            if destination == 'screen':
                self._write_to_screen(report_content)
            else:
                self._write_to_file(destination, report_content)

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
