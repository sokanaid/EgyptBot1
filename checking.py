def is_number_of_people(number):
    if not number.isdigit() or number < 0:
        return False
    else:
        return True
