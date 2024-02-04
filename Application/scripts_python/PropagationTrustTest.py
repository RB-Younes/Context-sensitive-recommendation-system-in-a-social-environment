import pandas as pn
import numpy as np

from Graph import Graph


def ex_prop(path):
    data = []
    for i in range(1508):
        for j in range(1508):
            data.append([i, j, 0])

    et_df = pn.DataFrame(data, columns=['user_1', 'user_2', 'ex'])

    # path = "C:/Users/LATITUDE/Desktop/FILM TRUST Users-Items-Ratings-Trust (csv's)/"
    FT_user_trustee_columns = ['user_1', 'user_2', 'ex']
    Data_exp_trust = pn.read_csv(path + 'ex_trust.csv', delimiter='::',
                                 names=FT_user_trustee_columns, engine='python')
    Data_exp_trust.user_1 = Data_exp_trust.user_1.astype(int)
    Data_exp_trust.user_2 = Data_exp_trust.user_2.astype(int)
    print(Data_exp_trust)

    piv = et_df.pivot(index='user_1', columns='user_2', values='ex')
    print(piv)

    for i in range(len(Data_exp_trust)):
        et_value = Data_exp_trust['ex'].iloc[i]
        piv.iloc[Data_exp_trust['user_1'].iloc[i], Data_exp_trust['user_2'].iloc[i]] = et_value

    g = Graph(len(piv))

    for i in range(len(piv)):
        for j in range(len(piv)):
            if piv.iloc[i, j] != 0:
                g.addEdge(i, j)

    for a in range(len(piv)):
        for b in range(len(piv)):
            if piv.iloc[a, b] == 0 and a != b:

                paths = g.printAllPaths(a, b)
                Val_1 = 0
                Val_2 = 0
                Trust_propagation = 0
                for i in range(len(paths)):
                    path = paths[i]
                    W_k = 1
                    Trust_value = 1
                    for j in range(len(path) - 1):
                        if j == 0:
                            s1 = path[j]
                        if j > 0:
                            s2 = path[j]
                            Trust_value = piv.iloc[s1, s2]
                            s1 = s2
                        W_k = W_k * Trust_value

                        s2 = path[j + 1]
                        W_direct = piv.iloc[s1, s2]

                    Val_1 = Val_1 + W_direct * W_k
                    Val_2 = Val_2 + W_k
                if Val_1 == 0 and Val_2 == 0:
                    Trust_propagation = 0
                else:
                    Trust_propagation = Val_1 / Val_2
                piv.iloc[a, b] = Trust_propagation
    print(piv)

    ex_prop_pivot = piv.unstack().reset_index(name='value')
    print(ex_prop_pivot)
    ex_prop_pivot.rename(columns={'user_2': 'user_1', 'user_1': 'user_2', 'value': 'ex_prop'}, inplace=True)
    print(ex_prop_pivot)
    # il manque un bout de code !!!!!
    ex_prop = ex_prop_pivot.unstack().reset_index(name='ex_prop')

    np.savetxt(path + 'ex_prop_trust.csv', ex_prop, delimiter='::', fmt='%f')
