# import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def calcule_theoreme_pythagore(a, b):
    c = np.sqrt(a**2 + b**2)
    return c

# # theoreme de pythagore
# a = 3
# b = 4
# c = calcule_theoreme_pythagore(a, b)
# print("Avec a = 3 et b = 4")
# print("Le côté c du triangle rectangle est de : ", c)

# # plot le triangle rectangle
# plt.plot([0, 0, a, 0], [0, b, 0, 0])
# plt.title("Triangle rectangle")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.grid()
# plt.axis('equal')
# plt.show()  

# exit()

# # plot an example of thereom de tales
# a = 3
# b = 4
# c = 5
# d = 6
# plt.plot([0, 0, a, 0], [0, b, 0, 0])
# plt.plot([0, 0, c, 0], [0, d, 0, 0])

# # show the plot
# plt.title("Theoreme de Tales")
# plt.xlabel("x")
# plt.ylabel("y")
# plt.grid()
# plt.axis('equal')
# plt.show()



# # theoreme de tales
a = 3
b = 4
c = 5
d = 6
e = (a * d) / b
# print("Avec a = 3, b = 4, c = 5 et d = 6")
# print("Le côté e du triangle est de : ", e)

# plot les geometries

# plot example of geometry
plt.plot([0, 0, a, 0], [0, b, 0, 0])
plt.plot([0, 0, c, 0], [0, d, 0, 0])
plt.plot([0, 0, a, 0], [0, d, 0, 0])
plt.plot([0, 0, c, 0], [0, b, 0, 0])
plt.plot([0, 0, a, 0], [0, e, 0, 0])
plt.plot([0, 0, c, 0], [0, e, 0, 0])
plt.show()


# # show the plot
# plt.show()  
