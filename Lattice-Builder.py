import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#Sets the position of the atoms of a Pyrochlore Lattice
# Will return a unit cell

def get_FCC(l, V):
    # l: lattice parameter
    # V: volume of unit cell
    # returns an array with pos. vectors

    e_1 = np.array([1,0,0])
    e_2 = np.array([0,1,0])
    e_3 = np.array([0,0,1])

    a_1 = 0.5*(e_1 + e_2)
    a_2 = 0.5*(e_2 + e_3)
    a_3 = 0.5*(e_3 + e_1)

    N = 4*V**3 # number of atoms in FCC

    atoms = np.zeros((N,3))
    FCCatoms = [0*e_1, a_1, a_2, a_3, 2*a_1, 2*a_2, 2*a_3, a_1 + a_2, a_2 + a_3, \
     a_1 + a_3, a_1 + a_2 + a_3, a_1 + a_2 - a_3, a_2 + a_3 - a_1, a_1 + a_3 - a_2]

    return FCCatoms

def get_diamonds(FCCatoms):

    diamonds = [[1/4,1/4,1/4] + p for p in FCCatoms]

    return diamonds

def get_pyrochlores(FCC):
    # Given an FCC lattice, return the position of the pyrochlore sites
    # Return as 3 different sets corresponding to points below:

    sites = [np.array([1/4,1/4,0]), np.array([0,1/4,1/4]), np.array([1/4,0,1/4])]

    set_1 = [v + sites[0] for v in FCC]
    set_2 = [v + sites[1] for v in FCC]
    set_3 = [v + sites[2] for v in FCC]

    return set_1, set_2, set_3

def find_NN(v, arr):
    # Given a diamond point find its nearest neighbours in FCC unit cell

    dist = [np.linalg.norm(p-v) for p in arr]
    min = np.amin(dist)
    print(np.where(dist == min)[0][0])
    return np.where(dist == min)[0][0]

def get_tetrahedron(p, s1, s2, s3):
    # Given a point p of the FCC lattice, find its nearest neighbors, 1 in each set
    return find_NN(p, s1), find_NN(p, s2), find_NN(p, s3)


def unit_cell():
    # returns the positions of atoms in n unit cells

    # First unit cell
    unit_FCC = get_FCC(1,1)
    unit_diamond = get_diamonds(unit_FCC)

    unit_p = get_pyrochlores(unit_FCC) # Contains 3 set of coordinates

    #tetrahedra = [] # each entry holds 4 points which lie in the same tetrahedron
    #visualization(unit_FCC, unit_p[0], unit_p[1], unit_p[2])
    unit_cell = [unit_FCC, unit_p]
    return unit_cell

def visualization(FCC, p1, p2, p3):
    xf = [v[0] for v in FCC]
    yf = [v[1] for v in FCC]
    zf = [v[2] for v in FCC]

    x1 = [v[0] for v in p1]
    y1 = [v[1] for v in p1]
    z1 = [v[2] for v in p1]

    x2 = [v[0] for v in p2]
    y2 = [v[1] for v in p2]
    z2 = [v[2] for v in p2]

    x3 = [v[0] for v in p3]
    y3 = [v[1] for v in p3]
    z3 = [v[2] for v in p3]

    i1, i2, i3 = get_tetrahedron(FCC[0], p1, p2, p3)

    c1 = p1[i1]; c2 = p2[i2]; c3 = p3[i3]
    print(c1, c2, c3, FCC[0])

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    #ax.scatter(xf, yf, zf, c = 'b')#, markersize = 14)
    #ax.scatter(x1, y1, z1, c = 'y')#, markersize = 14)
    #ax.scatter(x2, y2, z2, c = 'r')
    #ax.scatter(x3, y3, z3, c = 'g')

    x = [FCC[0][0], c3[0], c2[0], c1[0]]
    y = [FCC[0][1], c3[1], c2[1], c1[1]]
    z = [FCC[0][2], c3[2], c2[2], c1[2]]
    #ax.plot(FCC[0], c1, c2)
    ax.scatter(x,y,z, marker = '^')
    #ax.plot(FCC[0], c3)
    #ax.plot(c1, c2)
    #ax.plot(c1, c3)
    #ax.plot(c2, c3)
    #ax.plot3D([0,0,0], [1,1,1])
    plt.show()
    return None

def vmd_out(arr):
    # output the file into form for VMD visualization
    s = ''
    with open("vmdpyrochlore.xyz", 'w') as f:
        s = str(len(arr)) + '\n'
        s += 'Point = 1 \n'
        for i in range(len(arr)):
            s += 's' + str(i) + ' '
            for j in range(len(arr[0])):
                s += str(arr[i][j]) + ' '
            s += '\n'
        print(s)
        f.write(s)

    return None


def main():
    fcc, pyro = unit_cell()
    pyro_all = np.concatenate((pyro[0], pyro[1], pyro[2]), axis = 0)
    t_lattice = []
    lattice = []
    for i in range(2):
        t_lattice.append(v + i*u for v in fcc, for u in [[1,0,0], [0,1,0], [1, 1, 0]])
        t_lattice.append(v + i*u for v in pyro_all, for u \
                        in [[1,0,0], [0,1,0], [1, 1, 0]])

    for i in range(2):
        lattice.append(v + i*[0,0,1] for v in )


    return None

main()
