import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def save_table_to_csv(table, filename, columns_names):
    wavelengths = list(table.keys())
    
    # Generate the correct path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'data', filename)
    
    with open(file_path, 'w') as f:
        # Write header
        f.write(','.join(columns_names) + '\n')
        
        # Write data rows
        for wave in wavelengths:
            n_data_columns = len(table[wave])
            n_rows_per_wave = table[wave][0].size
            
            for j in range(n_rows_per_wave):
                row_data = [str(wave)]
                for i in range(n_data_columns):
                    row_data.append(str(table[wave][i][j]))
                f.write(','.join(row_data) + '\n')
    
    print(f'Table saved to {file_path}')



class read_csv:
    def __init__(self, filename):

        # Generate the correct path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'data', filename)


        self.data = pd.read_csv(file_path)
        self.wavelengths = self.data[self.data.columns[0]].unique()
        self.generate_table()
        
    def generate_table(self):
        self.table = {}
        columns = self.data.columns.size
        for wave in self.wavelengths:
            c = []
            for i in range(columns):
                column_data = self.data[self.data.columns[i]][self.data[self.data.columns[0]] == wave].values
                c.append(column_data)
            self.table[wave] = c

    def columns(self):
        return self.data.columns.values


if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, 'data', 'pab0.csv')
    print(data_path)
    my_csv = read_csv(data_path)
    my_csv = read_csv('./data/pab0.csv')
    
    table = my_csv.table
    print(table[665][0].size)
    
    print(my_csv.columns())
    print(my_csv.columns().size)
    print(my_csv.wavelengths)
    columns_names = ['Wavelength (nm)', 'Power (mW)', 'Counts', 'Dark Counts']

    save_table_to_csv(table, './data/pab_test.csv', columns_names)

