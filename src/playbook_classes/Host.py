class Host:
    """The class, which represents the host in the header
    """
    def __init__(self, name):
        """The constructor

        Args:
            name (string): name of the host
        """
        self.name = name

    def __str__(self):
        """Returns the string representation of the Host object

        Returns:
            string: Returns the string representation of the Host object
        """
        return self.name