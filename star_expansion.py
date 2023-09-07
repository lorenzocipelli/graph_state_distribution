from netqasm.sdk.external import Socket, NetQASMConnection
from netqasm.sdk import Qubit

def y_measurement(qubits: list[Qubit], conn: NetQASMConnection) :
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
        conn.flush()
    
    #conn.flush()
    return qubits

def vertex_deletion(a_0_qubit: Qubit, conn: NetQASMConnection):
    """
        rimozione del qubit a_0 nel caso di non appartenenza del nodo
        all'insieme W. Ottenuto attraverso misurazione del qubit a_0 
        nella base Z (base computazionale)
    """
    a_0_qubit.measure() # Z-basis measurement
    conn.flush()
    return a_0_qubit

def local_complementation(a_0_qubit: Qubit, c_i_qubits: list[Qubit], center_socket: Socket, conn: NetQASMConnection):
    """
        al qubit a_0 (entangled con il futuro centro stella) 
        viene applicata una rotazione rispetto all'asse X di -pi/4; 
        mentre, ai nodi localmente entangled fra di loro (nodi c_i)
        viene applicata una rotazione rispetto all'asse Z di pi/4
    """
    a_0_qubit.rot_X(3,2) # 3pi/4 == -pi/4
    conn.flush()
    center_socket.send("rot_Z")
    for c_i in c_i_qubits :
        c_i.rot_Z(1,2) # pi/4

    conn.flush() # per poter ricevere il messaggio successivo [sincronizzazione]
    center_socket.recv() # sincronizzazione
    return a_0_qubit, c_i_qubits

def remove_a0_local_edges(a_0_qubit: Qubit, c_i_qubits: list[Qubit], conn: NetQASMConnection):
    """
        rimozione dell'entanglement fra il qubit a_0 e tutti gli altri
        qubit presenti all'interno del nodo: attraverso gate CZ
    """
    for c_i in c_i_qubits :
        a_0_qubit.cphase(c_i)

    conn.flush()
    return a_0_qubit, c_i_qubits

def local_edge_addition(local_qubits: list[Qubit], conn: NetQASMConnection):
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

    conn.flush()
    return local_qubits[0], local_qubits[1:]

def star_expansion(a_0_qubit: Qubit, c_i_qubits: list[Qubit], belongs_W: bool, center_classic_socket: Socket, conn: NetQASMConnection):
    ''' 1) local_complementation()\n
        2) vertex_deletion() OR edge_addition()\n
        3) y_measurement
    '''
    a_0_qubit, c_i_qubits = local_edge_addition([a_0_qubit] + c_i_qubits, conn)
    a_0_qubit, c_i_qubits = local_complementation(a_0_qubit, c_i_qubits, center_classic_socket, conn)
    if belongs_W:
        a_0_qubit, c_i_qubits = remove_a0_local_edges(a_0_qubit, c_i_qubits, conn)
    else:
        a_0_qubit = vertex_deletion(a_0_qubit, conn)
    c_i_qubits = y_measurement(c_i_qubits, conn)
    conn.flush()
    return a_0_qubit, c_i_qubits






    