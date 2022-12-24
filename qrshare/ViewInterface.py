class ViewInterface(object):
    """An interface for classes that define a view for displaying text.

    This interface defines a method for validating the parameters passed to
    the constructor, as well as a method for displaying a string.
    """

    def __init__(self, *args):
        """Initialize the view with the given arguments."""
        super(ViewInterface, self).__init__(*args)

    @staticmethod
    def validate_init_params(**params):
        """Validate the parameters passed to the constructor.

        This method should check that the required parameters are present and have
        valid values, and raise an exception if any of the parameters are invalid.
        """
        pass

    def view(self, str):
        """Display the given string.

        This method should display the string in some way, such as printing it to
        the console or rendering it in a GUI window.
        """
        raise NotImplementedError()
