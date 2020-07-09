import matplotlib.pyplot as plt

data = [[1,2,3,4],[6,5,4,3],[1,3,5,1]]

table = plt.table(cellText=data, colLabels=['-', 'igG', 'igM', 'PCR'], loc='center', 
                  cellLoc='center')
table.auto_set_font_size(False)

plt.title("Acuracia Exames X Modelos")
plt.axis('off')
plt.show()