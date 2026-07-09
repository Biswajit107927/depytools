#Transpose IT. [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

transposed=[]

for row in range(len(matrix[0])):
    new_row=[]
    for column in range(len(matrix)):
        new_row.append(matrix[column][row])
    transposed.append(new_row)

print(transposed)


