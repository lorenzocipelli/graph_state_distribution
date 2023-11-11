from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket, Qubit
from star_expansion import dictionary, update_json, star_expansion_neighbour, label
import json
def main(app_config=None, belongs_W=True, other_nodes=[]):

    epr_sock = {}

    erin_sock = Socket("alice", "erin", log_config=app_config.log_config)
    charlie_sock = Socket("alice", "charlie", log_config=app_config.log_config)
    bob_sock = Socket("alice", "bob", log_config=app_config.log_config)

    for element in other_nodes:
        epr_sock[element] = EPRSocket(element)

    alice = NetQASMConnection(
        "alice",
        log_config=app_config.log_config,
        epr_sockets=list(epr_sock.values()),
    )
    with alice:
        q_ent_erin : Qubit = epr_sock["erin"].recv_keep()[0]
        q_ent_erin.H()
        
        alice.flush()

        """ 
            questi tre blocchi di codice successivi servono allo Star Expansion corrispettivo di:
            Erin -> Charlie -> Bob
            per poter effettuare le rotazioni sull'asse Z in maniera sincronizzata
            vengono attivati dai codici di Local Complementation nello Star Expansion
            se ne trovano 3 su Alice perchè Alice è il centro stella e quindi sicuramente
            ad ogni iterazione dello SE dovrà effettuare rotazione Z sul proprio qubit
            (che è remoto rispetto al nodo su cui effettivamente si sta effettuando lo SE,
            per questo che è necessaria la sincronizzazione)
        """
        star_expansion_neighbour(conn=alice,
                            communicating_socket=erin_sock,
                            qubit_to_rotate=q_ent_erin)

        star_expansion_neighbour(conn=alice,
                            communicating_socket=charlie_sock,
                            qubit_to_rotate=q_ent_erin)

        star_expansion_neighbour(conn=alice,
                            communicating_socket=bob_sock,
                            qubit_to_rotate=q_ent_erin)
        
        bob_sock.recv()

        m_erin = q_ent_erin.measure() # basis=0 -> X ; basis=1 -> Y ; basis=2 -> Z 

    #print("Alice measure -> " + str(label["alice"]))
    #dictionary["alice"].append(int(out))
    #update_json()
    
    #return {"measured": int(out)}

if __name__ == "__main__":
    main()