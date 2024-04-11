from sys import stdin, stdout
from operator import itemgetter

class gaussian(object):
    def __init__(self, mtx, out, error_rate=0.01, injection_rate=0.10):
        self.__mtx = mtx
        self.__out = out
        self.__error_rate = error_rate
        self.__injection_rate = injection_rate

    def run(self):
        import numpy as np
        from scipy.io import mmread, mmwrite
        from scipy.sparse import csr_matrix

        def read_mtx(file_path):
            dense_matrix = mmread(file_path)
            csr_data = csr_matrix(dense_matrix)
            return csr_data.toarray()

        def write_mtx(bin_data, mtx_file_path):
            csr_data = csr_matrix(bin_data)
            mmwrite(mtx_file_path, csr_data)


        def add_gaussian_noise_symmetric(matrix, error_rate, injection_rate, mean, std_dev):
            rows, cols = np.shape(matrix)

            # Find the position of a non-zero element.
            non_zero_indices = [(i, j) for i in range(rows) for j in range(i, cols) if matrix[i][j] != 0]

            # Calculate number of elements to inject noise (only for non-zero elements)
            num_noisy_elements = int(np.ceil(len(non_zero_indices) * injection_rate))

            # Randomly select an element to inject noise from among the non-zero elements
            noisy_indices = np.random.choice(range(len(non_zero_indices)), num_noisy_elements, replace=False)

            # Create an empty matrix to add errors to.
            noise_matrix = np.zeros((rows, cols))

            # Add Gaussian noise to selected locations
            for index in noisy_indices:
                i, j = non_zero_indices[index]  # Convert to actual matrix index

                # Gaussian noise generation
                noise = np.random.normal(mean, std_dev)

                # Noise adjustment based on error rate
                noise = noise * error_rate

                # Add noise (maintain symmetry)
                noise_matrix[i][j] = noise
                noise_matrix[j][i] = noise  # Same noise applies to symmetrical elements

            # Add a noise matrix to the original matrix.
            result_matrix = np.add(matrix, noise_matrix)

            return result_matrix

        infile = open(self.__mtx, "rb")
        outfile = open(self.__out, "wb")

        A = read_mtx(infile)

        # Extract non-zero elements
        non_zero_elements = A[A != 0]

        # Calculate parameters of Gaussian distribution
        mean = np.mean(non_zero_elements)
        std_dev = np.std(non_zero_elements)

        # Create a matrix with added noise
        noisy_matrix = add_gaussian_noise_symmetric(A, self.__error_rate,
                                                    self.__injection_rate, mean, std_dev)

        write_mtx(noisy_matrix, outfile)
