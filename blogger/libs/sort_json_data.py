



def sort(data, value):
    '''
    Sort the Json data in asscending order using given value.
    '''
    sorted_data =  sorted(data, key = lambda i: i[value])
    return sorted_data