class Parser(object):
    """
    A sample dummy parser to showcase how to represent
    the parser code
    """

    def __init__(self, data_dir=None):
        """
        Constructor: @data_dir is an optional parameter that is passed in
        by the parser tester. This data dir can contain any data files that
        the parser needs to perform its operations when `parse` function is
        called.
        """
        pass

    def parse(self, x):
        """
        This parse function is called by parser tester once per input line.
        The response can be any basic python data type that represents the
        result of parsing the input string @x
        """
        return x.lower()
