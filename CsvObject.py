class CsvObject(object):
    def __init__(self, number_of_rows, number_of_columns):
        self.number_of_rows = number_of_rows
        self.number_of_columns = number_of_columns
        self.data = 

    def __getitem__(self, row_number):
        return self.data[row_number]