from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket


def main(app_config=None, belongs_W=True, other_nodes=[]):

    epr_sock = {}
    charlie_sock = Socket("david", "charlie", log_config=app_config.log_config)

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
            questo bloccho di codice serve allo Star Expansion corrispettivo di: Charlie
            per poter effettuare le rotazioni sull'asse Z in maniera sincronizzata
            vengono attivati dai codici di Local Complementation nello Star Expansion
            se ne trovano 1 su David perchè David è collegato con Charlie e quindi sicuramente
            per la sua iterazione dello SE dovrà effettuare rotazione Z sul proprio qubit
            (che è remoto rispetto al nodo su cui effettivamente si sta effettuando lo SE,
            per questo che è necessaria la sincronizzazione)
        """
        msg = charlie_sock.recv()
        while (msg == "rot_Z") :
            q_ent_charlie.rot_Z(1,2) # pi/4
            david.flush()
            charlie_sock.send("done_rot_Z")
            msg = charlie_sock.recv()

    # Print the outcome
    #print(f"david's outcome with Bob is: {m}")


if __name__ == "__main__":
    main()