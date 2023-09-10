from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from star_expansion import star_expansion_neighbour


def main(app_config=None, belongs_W=True, other_nodes=[]):
    
    epr_sock = {}
    bob_sock = Socket("frank", "bob", log_config=app_config.log_config)

    for element in other_nodes:
        epr_sock[element] = EPRSocket(element)
   
    frank = NetQASMConnection(
        "frank",
        log_config=app_config.log_config,
        epr_sockets= list(epr_sock.values()),
    )
    with frank:
        q_ent_bob = epr_sock["bob"].recv_keep()[0]
        q_ent_bob.H()

        frank.flush()

        """ 
            questo bloccho di codice serve allo Star Expansion corrispettivo di: Bob
            per poter effettuare le rotazioni sull'asse Z in maniera sincronizzata
            vengono attivati dai codici di Local Complementation nello Star Expansion
            se ne trovano 1 su Frank perchè Frank è collegato con Bob e quindi sicuramente
            per la sua iterazione dello SE dovrà effettuare rotazione Z sul proprio qubit
            (che è remoto rispetto al nodo su cui effettivamente si sta effettuando lo SE,
            per questo che è necessaria la sincronizzazione)
        """
        star_expansion_neighbour(conn=frank,
                            communicating_socket=bob_sock,
                            qubit_to_rotate=q_ent_bob)

if __name__ == "__main__":
    main()