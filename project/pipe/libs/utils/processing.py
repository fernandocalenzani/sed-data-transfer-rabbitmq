import pickle

import matplotlib.pyplot as plt


class Processing:
    def bytes_to_matrix(self, byte_data):
        deserialized_data = pickle.loads(byte_data)
        return deserialized_data

    def show_image(self, matrix):
        plt.imshow(matrix)
        plt.show()
