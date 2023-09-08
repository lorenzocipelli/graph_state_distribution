from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket


def main(app_config=None, belongs_W=True, other_nodes=[]):

    epr_sock = {}
    erin_sock = Socket("gary", "erin", log_config=app_config.log_config)

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
            questo bloccho di codice serve allo Star Expansion corrispettivo di: Erin
            per poter effettuare le rotazioni sull'asse Z in maniera sincronizzata
            vengono attivati dai codici di Local Complementation nello Star Expansion
            se ne trovano 1 su Gary perchè Gary è collegato con Erin e quindi sicuramente
            per la sua iterazione dello SE dovrà effettuare rotazione Z sul proprio qubit
            (che è remoto rispetto al nodo su cui effettivamente si sta effettuando lo SE,
            per questo che è necessaria la sincronizzazione)
        """
        msg = erin_sock.recv()
        while (msg == "rot_Z") :
            q_ent_erin.rot_Z(1,2) # pi/4
            gary.flush()
            erin_sock.send("done_rot_Z")
            msg = erin_sock.recv()

if __name__ == "__main__":
    main()