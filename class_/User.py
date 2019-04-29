""" vim: set et sw=4 ts=4 sts=4:

User class
Just tracks user information

"""

class User:
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
        """ Return mixed
        if var is None, return dict with all user data
        otherwise return the field specified by var if valid
        If not valid, returns False
        """

        if var is None:
            return {x:y for x,y in self.__data.items()}

        if var not in self.__data:
            return False

        return self.__data[var]

    @staticmethod
    def get_field_names():
        return [x for x in User.__data]
