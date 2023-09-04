def y_measurement(qubits) :
    """
        misurazione rispetto alla base Y su un nodo che corrisponde
        graficamente alla complementazione locale su qual nodo con 
        successiva eliminazione del nodo su cui essa è stata applicata
        (rimane solamente il sottografo conseguenza della LC)
    """
    for q in qubits :
        q.rot_Z(3,1) # S^dagger, 3pi/2 == -pi/2
        q.H()
        q.measure() # Y-basis measurement

def vertex_deletion(a_0_qubit):
    """
        rimozione del qubit a_0 nel caso di non appartenenza del nodo
        all'insieme W. Ottenuto attraverso misurazione del qubit a_0 
        nella base Z (base computazionale)
    """
    a_0_qubit.measure()

def local_complementation(a_0_qubit, c_i_qubits):
    """
        al qubit a_0 (entangled con il futuro centro stella) 
        viene applicata una rotazione rispetto all'asse X di -pi/4; 
        mentre, ai nodi localmente entangled fra di loro (nodi c_i)
        viene applicata una rotazione rispetto all'asse Z di pi/4
    """
    a_0_qubit.rot_X(3,2) # 3pi/4 == -pi/4
    for c_i in c_i_qubits :
        c_i.rot_Z(1,2) # pi/4

def remove_a0_local_edges(a_0_qubit, c_i_qubits):
    """
        rimozione dell'entanglement fra il qubit a_0 e tutti gli altri
        qubit presenti all'interno del nodo: attraverso gate CZ
    """
    for c_i in c_i_qubits :
        a_0_qubit.cphase(c_i)

def local_edge_addition(local_qubits):
    """
        tutti i qubits a_i, i>=0 di A (nodo) sono linkati utilizzato CZ tra
        tutte le possibili coppie. La funzione effettua esattamente
        [n*(n-1)]/2 passaggi
    """
    n_qubits = len(local_qubits)
    # se ho 5 qubits faccio 4 iterazioni
    for x in range(n_qubits-1) :
        # se sono arrivato alla seconda iterazione con 5 qubits
        # faccio solamente 3 iterazioni, 2_qubit.cphase(3_qubit)
        # 2_qubit.cphase(4_qubit), 2_qubit.cphase(5_qubit)
        for y in range(n_qubits-1-x) :
            # print("X: " + str(x) + "\nY: " + str(y) + 
            #     "\nQubit " + str(x) + " cphase with " + str(x+y+1)) # debug
            local_qubits[x].cphase(local_qubits[x+y+1])

def star_expansion(a_0_qubit, c_i_qubits, belongs_W):
    ''' local_complementation()
        vertex_deletion() OR edge_addition()
        y_measurement
    '''
    local_qubits = [a_0_qubit] + c_i_qubits # concat
    local_edge_addition(local_qubits)
    local_complementation(a_0_qubit, c_i_qubits)
    if belongs_W:
        remove_a0_local_edges(a_0_qubit, c_i_qubits)
    else:
        vertex_deletion(a_0_qubit)
    y_measurement(c_i_qubits)






    