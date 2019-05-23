""" vim: set et sw=4 ts=4 sts=4: """


class User:
    """
    A class used to represent the User

    Attributes
    ----------
    user_id : string
        the users identification number
    username : string
        the users login username
    first_name : string
        first name of the user
    surname : string
        last name of the user
    email : string
        the users email address
    """

    __data = {
        'user_id': None,
        'username': None,
        'first_name': None,
        'surname': None,
        'email': None
    }

    def __init__(
            self,
            user_id=None,
            username=None,
            first_name=None,
            surname=None,
            email=None):

        self.__data['user_id'] = user_id
        self.__data['username'] = username
        self.__data['first_name'] = first_name
        self.__data['surname'] = surname
        self.__data['email'] = email

    def get_info(self, var=None):
        """
        A fuction created to return specified information

        Args:
            var: the information being requested

        Returns:
            if var is none, a dict with all user date
            if var is specified return the feild specified by var
            else return False
        """

        if var is None:
            return {x: y for x, y in self.__data.items()}

        if var not in self.__data:
            return False

        return self.__data[var]

    @staticmethod
    def get_field_names():
        return [x for x in User.__data]
