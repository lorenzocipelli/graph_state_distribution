from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from star_expansion import dictionary, star_expansion_neighbour, update_json, label


def main(app_config=None, belongs_W=True, other_nodes=[]):

    epr_sock = {}
    
    erin_sock = Socket("gary", "erin", log_config=app_config.log_config)
    bob_sock = Socket("gary", "bob", log_config=app_config.log_config)

    for element in other_nodes:
        epr_sock[element] = EPRSocket(element)

    gary = NetQASMConnection(
        "gary",
        log_config=app_config.log_config,
        epr_sockets=list(epr_sock.values()),
    )
    with gary:
        q_ent_erin = epr_sock["erin"].recv_keep()[0]
        q_ent_erin.H()

        gary.flush()

        """ 
            questo blocco di codice serve allo Star Expansion corrispettivo di: Erin
            per poter effettuare le rotazioni sull'asse Z in maniera sincronizzata
            vengono attivati dai codici di Local Complementation nello Star Expansion
            se ne trovano 1 su Gary perchè Gary è collegato con Erin e quindi sicuramente
            per la sua iterazione dello SE dovrà effettuare rotazione Z sul proprio qubit
            (che è remoto rispetto al nodo su cui effettivamente si sta effettuando lo SE,
            per questo che è necessaria la sincronizzazione)
        """
        star_expansion_neighbour(conn=gary,
                            communicating_socket=erin_sock,
                            qubit_to_rotate=q_ent_erin)
        
        bob_sock.recv()
        if label['gary']['erin']['label'] == 1:
            q_ent_erin.X()
            q_ent_erin.Z()

        if label['gary']['erin']['shape'] == 1:
            q_ent_erin.S()
        
        m_erin = q_ent_erin.measure()
    
    print("Gary measure -> " + str(int(m_erin)))
    #rw_json("Gary", m_erin)
    
    #dictionary["gary"].append(out)
    #update_json()
    #print("Gary measure -> " + str(out))
    #return {"measured": int(out)}

if __name__ == "__main__":
    main()