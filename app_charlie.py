from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from star_expansion import star_expansion, local_edge_addition, remove_a0_local_edges, local_complementation, vertex_deletion, y_measurement


def main(app_config=None, belongs_W=True, other_nodes=[]):

    epr_sock = {}

    for element in other_nodes:
        epr_sock[element] = EPRSocket(element)

    charlie = NetQASMConnection(
        "charlie",
        log_config=app_config.log_config,
        epr_sockets=list(epr_sock.values()),
    )
    with charlie:
        # Receive an entangled pair using the EPR socket to bob
        q_ent_bob = epr_sock["bob"].recv_keep()[0]
        q_ent_bob.H()
        q_ent_erin = epr_sock["erin"].recv_keep()[0]
        q_ent_erin.H()
        q_ent_david = epr_sock["david"].recv_keep()[0]
        q_ent_david.H()
        charlie.flush()
        #aggiungo alice ma non so se è necessario: in teoria è già connessa tramite la star expansion eseguita in erin
        
        #print("charlie star expansion start")
        #star_expansion(q_ent_erin, [q_ent_bob, q_ent_david], belongs_W)
        #charlie.flush()
        #print("charlie star expansion end")

    # Print the outcome
    #print(f"charlie's outcome with Bob is: {m}")

    # Send the outcome to alice
    #socket.send(str(m))

if __name__ == "__main__":
    main()