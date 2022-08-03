import numpy as np


def create_matrix(order):
    if order == 1:
        dims_1 = input("Enter size of first matrix: ")
        dims_1 = dims_1.replace(' ', '')
        matrix_1 = np.zeros((int(dims_1[0]), int(dims_1[1])))
        print("Enter first matrix: ")
        i = 0
        for x in range(int(dims_1[0])):
            row = input()
            matrix_1[i] = np.fromstring(row, dtype='float64', sep=' ')
            i += 1
        return matrix_1

    elif order == 2:
        dims_2 = input("Enter size of second matrix: ")
        dims_2 = dims_2.replace(' ', '')
        matrix_2 = np.zeros((int(dims_2[0]), int(dims_2[1])))
        print("Enter second matrix: ")
        i = 0
        for x in range(int(dims_2[0])):
            row = input()
            matrix_2[i] = np.fromstring(row, dtype='float64', sep=' ')
            i += 1
        return matrix_2

    elif order == 3:
        dims_3 = input("Enter size of matrix: ")
        dims_3 = dims_3.replace(' ', '')
        matrix_3 = np.zeros((int(dims_3[0]), int(dims_3[1])))
        print("Enter matrix: ")
        i = 0
        for x in range(int(dims_3[0])):
            row = input()
            matrix_3[i] = np.fromstring(row, dtype='float64', sep=' ')
            i += 1
        return matrix_3


def print_without_brackets(matrix):
    i = 0
    for x in matrix:
        for j in x:
            if i < (len(matrix[0]) - 1):
                print(j, end=" ")
                i += 1
            else:
                print(j)
                i = 0


while True:
    print("\n1. Add matrices")
    print("2. Multiply matrix by a constant")
    print("3. Multiply matrices")
    print("4. Transpose matrix")
    print("5. Calculate a determinant")
    print("6. Inverse matrix")
    print("0. Exit")
    choice = input("Your choice: ")
    choice = choice.replace(' ', '')
    if choice == '1':
        matrix_1 = create_matrix(1)
        matrix_2 = create_matrix(2)
        final_matrix = matrix_1 + matrix_2
        print_without_brackets(final_matrix)
    elif choice == '2':
        matrix_1 = create_matrix(1)
        multiply_factor = float(input("Enter constant: "))
        print("The result is: ")
        final_matrix = matrix_1 * multiply_factor
        print_without_brackets(final_matrix)
    elif choice == '3':
        matrix_1 = create_matrix(1)
        matrix_2 = create_matrix(2)
        final_matrix = matrix_1.dot(matrix_2)
        print_without_brackets(final_matrix)
    elif choice == '4':
        print("\n1. Main diagonal")
        print("2. Side diagonal")
        print("3. Vertical line")
        print("4. Horizontal line")
        transpose_choice = input("Your choice: ")
        if transpose_choice == '1':
            matrix_1 = create_matrix(3)
            final_matrix = matrix_1.transpose()
            print("The result is: ")
            print_without_brackets(final_matrix)
        elif transpose_choice == '2':
            matrix_1 = create_matrix(3)
            matrix_1 = np.transpose(matrix_1)
            final_matrix = np.flip(matrix_1)
            print("The result is: ")
            print_without_brackets(final_matrix)
        elif transpose_choice == '3':
            matrix_1 = create_matrix(3)
            i = 0
            while i < len(matrix_1) / 2:
                matrix_1[:, [i, len(matrix_1) - 1 - i]] = matrix_1[:, [len(matrix_1) - 1 - i, i]]
                i += 1
            print("The result is: ")
            print_without_brackets(matrix_1)
        elif transpose_choice == '4':
            matrix_1 = create_matrix(3)
            i = 0
            while i < len(matrix_1) / 2:
                matrix_1[[i, len(matrix_1) - 1 - i]] = matrix_1[[len(matrix_1) - 1 - i, i]]
                i += 1
            print("The result is: ")
            print_without_brackets(matrix_1)
    elif choice == '5':
        matrix_1 = create_matrix(3)
        (sign, logdet) = np.linalg.slogdet(matrix_1)
        det = sign * np.exp(logdet)
        print("The result is: ")
        print(det)
    elif choice == '6':
        matrix_1 = create_matrix(3)
        (sign, logdet) = np.linalg.slogdet(matrix_1)
        det = sign * np.exp(logdet)
        if det != 0:
            matrix_1 = np.linalg.inv(matrix_1)
            print("The result is: ")
            print_without_brackets(matrix_1)
        else:
            print("This matrix doesn't have an inverse.")
    elif choice == '0':
        break

