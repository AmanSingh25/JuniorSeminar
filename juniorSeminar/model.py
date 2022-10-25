import csv

def retrieve_csv_data(csv_file):
    """ Function will retrieve the csv data and read it.
    Args: No arguments.
    Returns: Returns 2D Array.
    """
    csv_file = open(csv_file)
    print(csv_file)
    csv_object = csv.reader(csv_file)

    graduation_list_info = []
    for row in csv_object:
        graduation_list_info.append(row)
    return graduation_list_info


def majors_at_fisk(csv_file):
    """ Function will return the unique majors list at Fisk.
    """
    unique_majors = set() 
    graduation_list_info = retrieve_csv_data(csv_file)

    for row in graduation_list_info:
        unique_majors.add(row[3].strip().upper())
    
    return sorted(list(unique_majors))


def is_all_empty(chars):
    '''
    this function checks if the input is empty and returnsw True
    args:set of characters
    return type: boolean
    '''
    if len(chars) == 0:
        return True
    return False

def is_valid_password(password):
    '''
    this function checks if the password has a certain minimunm length and contains alphanumeric characters, also contains special chars
    args: password
    return type: boolean, returns true if password has one upper case, one lower case, one special char and one numeric character. 
    '''
    if len(password) < 5:
        raise ValueError("Password's length must be at least 5 characters. ")
    if type(password) != str:
        raise TypeError("Password must be a string")

    special_char = 0
    upper_case = 0
    lower_case = 0
    num = 0

    for chars in password:
        if chars.isdigit():
            num += 1
        elif chars.isupper():
            upper_case += 1
        elif chars.islower():
            lower_case += 1
        elif chars in {"@", "$", "!", "^", "&", "*", "#"}:
            special_char += 1
    
    if special_char > 0 and lower_case > 0 and upper_case > 0 and num > 0:
        return True
    return False