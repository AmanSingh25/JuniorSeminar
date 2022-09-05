import csv

def retrieve_csv_data(csv_file):
    """ Function will retrieve the csv data and read it.
    Args: No arguments.
    Returns: Returns 2D Array.
    """
    csv_file = open(csv_file)
    csv_object = csv.reader(csv_file)

    graduation_list_info = []
    for row in csv_object:
        graduation_list_info.append(row)
    
    return graduation_list_info


def majors_at_fisk(csv_file):
    """ Function will return the unique majors at Fisk.
    """
    unique_majors = set() 
    graduation_list_info = retrieve_csv_data(csv_file)

    for row in graduation_list_info:
        unique_majors.add(row[3].strip().upper())
    
    return sorted(list(unique_majors))
