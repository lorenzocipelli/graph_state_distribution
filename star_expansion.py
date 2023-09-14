from netqasm.sdk.external import Socket, NetQASMConnection
from netqasm.sdk import Qubit
import json 

f = open('results.json')
dictionary = json.load(f)
f.close()

e = open("errors.json")
errors_tracker = json.load(e)
e.close()


class QubitSocket:
  """
    Classe da utilizzare quando si vuole effettuare lo Star Expansion. Infatti, il metodo per l'SE accetta
    come input solamente questa classe che ci permette di accoppiare il Qubit locale alla Socket classica
    in modo da effettuare le dovute sincronizzazioni per portare avanti la Complementazione Locale all'interno
    dell'SE (sia nel passaggio LC che nella misurazione in base Y)
  """
  def __init__(self, local_qubit: Qubit, classic_socket: Socket):
    self.local_qubit = local_qubit
    self.classic_socket = classic_socket

def star_expansion_neighbour(conn: NetQASMConnection, communicating_socket: Socket, qubit_to_rotate: Qubit) :
    """ 
        Metodo da utilizzare ogni volta che su un nodo vicino avviene l'operazione di Star Expansion.
        Questa funzione permette di effettuare sul qubit vicino (quello su cui viene chiamata la funzione) le
        rotazioni necessarie per la riuscita corretta dei Local Complementation dell'SE (sia nell'LC sul qubit a_0
        che quelli effettuati per la misurazione in base Y).\n
        IMPORTANTE: ricordarsi di utilizzare OGNI volta che un nodo vicino sta effettuando lo Star Expansion
    """
    msg = communicating_socket.recv()
    while (msg == "rot_Z") :
        qubit_to_rotate.rot_Z(3,1) # pi/4 = rot_Z(1,2) | pi/2 = rot_Z(1,1) | -pi/2 = 3pi/2 = rot_Z(3,1)
        conn.flush()
        communicating_socket.send("done_rot_Z")
        msg = communicating_socket.recv()


def y_measurement(a_0_qubit: QubitSocket, to_delete_qubits: list[QubitSocket], conn: NetQASMConnection) :
    """
        Misurazione rispetto alla base Y su un nodo che corrisponde
        graficamente alla complementazione locale su quel nodo con 
        successiva eliminazione del nodo su cui essa è stata applicata
        (rimane solamente il sottografo conseguenza della LC)
    """

    """ 
        il blocco di codice successivo utilizza il metodo grafico coincidente con
        la misurazione in base Y: LC seguita dalla rimozione del vertice misurato.
        Come si può notare, ogni nodo locale c_i collega esattamente con il nodo che diventerà
        centro stella e con un altro nodo esterno, su questi due esterni andrà fatta la rotazione Z
        mentre su se stesso la rotazione X. Seguita poi dalla Vertex Deletion...
    """
    for to_delete in to_delete_qubits :
        to_delete.local_qubit.rot_X(1,1) # 3pi/4 == -pi/4
        to_delete.classic_socket.send("rot_Z") # ordina al qubit NON locale di fare rotazione
        conn.flush() # per poter ricevere il messaggio successivo [sincronizzazione]
        to_delete.classic_socket.recv() # attendo l'avvenuta rotazione
        a_0_qubit.classic_socket.send("rot_Z")
        conn.flush() # per poter ricevere il messaggio successivo [sincronizzazione]
        a_0_qubit.classic_socket.recv() # attendo l'avvenuta rotazione

    """ 
        fermo le altre applicazioni dall'ascolto dei messaggi, in dettaglio,
        questi send vanno a fermare quei while che ci sono all'interno
        delle applicazioni sui nodi che sono a contatto con il nodo su 
        cui si sta facendo star expansion
    """
    a_0_qubit.classic_socket.send("end")
    for to_delete in to_delete_qubits :
        to_delete.classic_socket.send("end")

    """ 
        elininazione definitiva dei qubit locali sul nodo (c_i)
    """
    for to_delete in to_delete_qubits :
        vertex_deletion(to_delete, conn)
        conn.flush()

    # VECCHIO CODICE, RIMPIAZZATO CON QUELLO DI SOPRA # # # # # # # # # # # # # # # # # #
    # il blocco di codice successivo permette l'utilizzo della misurazione in base Y
    # fatta attraverso gate S^dagger seguito da Hadamard ed infine misurazione
    # for q in qubits :
    #     q.rot_Z(3,1) # S^dagger, 3pi/2 == -pi/2
    #     q.H()
    #     q.measure() # Y-basis measurement
    #     conn.flush()
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


def vertex_deletion(a_0_qubit: QubitSocket, conn: NetQASMConnection):
    """
        Rimozione del qubit a_0 nel caso di non appartenenza del nodo
        all'insieme W. Ottenuto attraverso misurazione del qubit a_0 
        nella base Z (base computazionale)
    """
    a_0_qubit.local_qubit.measure() # Z-basis measurement
    conn.flush()


def remove_a0_local_edges(a_0_qubit: QubitSocket, c_i_qubits: list[QubitSocket], conn: NetQASMConnection):
    """
        Rimozione dell'entanglement fra il qubit a_0 e tutti gli altri
        qubit presenti all'interno del nodo: attraverso gate CZ
    """
    for c_i in c_i_qubits :
        a_0_qubit.local_qubit.cphase(c_i.local_qubit)

    conn.flush()


def local_complementation(a_0_qubit: QubitSocket, c_i_qubits: list[QubitSocket], conn: NetQASMConnection):
    """
        Al qubit a_0 (entangled con il futuro centro stella) 
        viene applicata una rotazione rispetto all'asse X di -pi/4; 
        mentre, ai nodi localmente entangled fra di loro (nodi c_i)
        viene applicata una rotazione rispetto all'asse Z di pi/4
    """
    a_0_qubit.local_qubit.rot_X(1,1) # 3pi/4 == -pi/4
    for c_i in c_i_qubits :
        c_i.local_qubit.rot_Z(3,1) # pi/4

    a_0_qubit.classic_socket.send("rot_Z")
    conn.flush() # per poter ricevere il messaggio successivo [sincronizzazione]
    a_0_qubit.classic_socket.recv() # sincronizzazione


def local_edge_addition(local_qubits: list[QubitSocket], conn: NetQASMConnection):
    """
        Tutti i qubits a_i, i>=0 di A (nodo) sono linkati utilizzato CZ tra
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
            local_qubits[x].local_qubit.cphase(local_qubits[x+y+1].local_qubit)

    conn.flush()

def star_expansion(a_0_qubit_socket: QubitSocket, c_i_qubit_socket: list[QubitSocket], belongs_W: bool, conn: NetQASMConnection):
    ''' 1) local_complementation()\n
        2) vertex_deletion() OR edge_addition()\n
        3) y_measurement
    '''
    print(conn.app_name.capitalize() + ": Star Expansion START")

    local_edge_addition([a_0_qubit_socket] + c_i_qubit_socket, conn)
    local_complementation(a_0_qubit_socket, c_i_qubit_socket, conn)
    if belongs_W:
        remove_a0_local_edges(a_0_qubit_socket, c_i_qubit_socket, conn)
    else:
        vertex_deletion(a_0_qubit_socket, conn)
    y_measurement(a_0_qubit_socket, c_i_qubit_socket, conn)

    print(conn.app_name.capitalize() + ": Star Expansion END")



counter = 0
def update_json():
    global counter
    if counter == 4: 
        with open("results.json", "w") as write_file:
            json.dump(dictionary, write_file)
        write_file.close()
        #controllo eventuali errori
        for k in dictionary:
            for i in range(0, len(dictionary["alice"])):
                if dictionary["alice"][i] != dictionary[k][i]:
                    errors_tracker[k] += 1
        with open("errors.json", "w") as write_file:
            json.dump(errors_tracker, write_file)
        write_file.close()
    else :
        counter += 1



