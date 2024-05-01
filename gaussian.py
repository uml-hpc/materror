from sys import stdin, stdout
from operator import itemgetter
import random
import numpy as np

class gaussian(object):
    def __init__(self, mtx, out, error_rate=0.01, injection_rate=0.10):
        self.__mtx = mtx
        self.__out = out
        self.__error_rate = error_rate
        self.__injection_rate = injection_rate

    def run(self):
        def read_mtx(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()
            matrix_data = [line.split() for line in lines if not line.startswith('%')]
            return ([l for l in lines if l.startswith('%')], matrix_data)

        def write_mtx(comments, lines, mtx_file_path):
            with open(mtx_file_path, 'w') as file:
                file.writelines(comments)
                for line in lines:
                    file.write(f"{' '.join(line)}\n")

        def point_gauss(value, error_rate):
            noise = np.random.normal(value, abs(value) * error_rate)
            return value + noise


        def add_gaussian_noise(matrix_data, error_rate, injection_rate):
			# Identify the data lines (excluding comments and the first line)
            header = matrix_data[0]

            # Skip the first line (dimensions)
            matrix_values = matrix_data[1:]

            # Determine the number of entries to modify (elements to inject noise)
            num_entries_to_modify = int(len(matrix_values) * injection_rate)

            # Randomly select entries to modify
            entries_to_modify = random.sample(matrix_values, num_entries_to_modify)

            # Add Gaussian noise to the selected entries
            for entry in entries_to_modify:
                entry[2] = str(point_gauss(float(entry[2]), error_rate))

            # Combine the comments, header, and modified data
            return [header] + matrix_values

        (comments, A) = read_mtx(self.__mtx)
        noisy_matrix = add_gaussian_noise(A, self.__error_rate, self.__injection_rate)
        write_mtx(comments, noisy_matrix, self.__out)
