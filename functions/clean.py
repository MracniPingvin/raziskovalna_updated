__author__ = 'FAMILY'

def reverse(shape):
    new=[]
    for i in shape:
        new.append(-i)
    return(new)

def clean(matrix_list):
    # cleans the list of possible solutions of those that are the same or could connect into different geometries
    clean_matrix_list=[]
    flag=True
    first=True
    # cleans all of the reflections, translations of the stable lattices that appeared during generation
    for i in matrix_list:
        if first==True:
            clean_matrix_list.append(i)
            first=False
        else:
            for j in clean_matrix_list:
                if i[0]==j[0] and i[1]==j[1] and i[5]==j[5]:
                    flag=False
                    break
                elif i[0]==j[0] and reverse(i[1])==j[1] and reverse(i[5])==j[5]:
                    flag=False
                    break
            if flag==True:
                clean_matrix_list.append(i)
            else:
                flag=True
    indexes=[]
    count=0
    # cleans all of the possible lattices with the same connection matrix, that connect into different geometries
    for i in clean_matrix_list:
        count=0
        for j in clean_matrix_list:
            if i[0]==j[0] and i!=j:
                if count not in indexes:
                    indexes.append(count)

                break
            count+=1

    list=[]
    true_matrix_list=[]

    for i in range(len(clean_matrix_list)):
        list.append(i)

    for i in list:
        if i not in indexes:
            true_matrix_list.append(clean_matrix_list[i])

    return true_matrix_list
