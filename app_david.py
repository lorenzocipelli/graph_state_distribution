from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from star_expansion import dictionary, update_json,star_expansion_neighbour, label


def main(app_config=None, belongs_W=True, other_nodes=[]):

    epr_sock = {}
    
    charlie_sock = Socket("david", "charlie", log_config=app_config.log_config)
    bob_sock = Socket("david", "bob", log_config=app_config.log_config)

    for element in other_nodes:
        epr_sock[element] = EPRSocket(element)

    david = NetQASMConnection(
        "david",
        log_config=app_config.log_config,
        epr_sockets=list(epr_sock.values()),
    )
    with david:
        q_ent_charlie = epr_sock["charlie"].create_keep()[0]
        q_ent_charlie.H()

        david.flush()

        """ 
            questo blocco di codice serve allo Star Expansion corrispettivo di: Charlie
            per poter effettuare le rotazioni sull'asse Z in maniera sincronizzata
            vengono attivati dai codici di Local Complementation nello Star Expansion
            se ne trovano 1 su David perchè David è collegato con Charlie e quindi sicuramente
            per la sua iterazione dello SE dovrà effettuare rotazione Z sul proprio qubit
            (che è remoto rispetto al nodo su cui effettivamente si sta effettuando lo SE,
            per questo che è necessaria la sincronizzazione)
        """
        star_expansion_neighbour(conn=david,
                            communicating_socket=charlie_sock,
                            qubit_to_rotate=q_ent_charlie)

        bob_sock.recv()
        if label['david']['charlie']['label'] == 1:
            q_ent_charlie.X()
            q_ent_charlie.Z()
        if label['david']['charlie']['shape'] == 1:
            q_ent_charlie.S()
        
        m_charlie = q_ent_charlie.measure()
    
    print("David measure -> " + str(int(m_charlie)))
    #rw_json("David", m_erin)
    
   #dictionary["david"].append(int(out))
    #update_json()
    #print("David measure -> " + str(out))
    #return {"measured": int(out)}

if __name__ == "__main__":
    main()