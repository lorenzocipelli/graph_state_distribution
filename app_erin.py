from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from star_expansion import star_expansion, local_edge_addition, remove_a0_local_edges, local_complementation, vertex_deletion, y_measurement


def main(app_config=None, belongs_W=True, other_nodes=[]):

    epr_sock = {}
    charlie_sock = Socket("erin", "charlie", log_config=app_config.log_config)

    for element in other_nodes:
        epr_sock[element] = EPRSocket(element)

    erin = NetQASMConnection(
        "erin",
        log_config=app_config.log_config,
        epr_sockets=list(epr_sock.values()),
    )
    with erin:
        # Receive an entangled pair using the EPR socket to bob
        q_ent_charlie = epr_sock["charlie"].create_keep()[0]
        q_ent_charlie.H()
        q_ent_alice = epr_sock["alice"].create_keep()[0]
        q_ent_alice.H()
        q_ent_gary = epr_sock["gary"].create_keep()[0]
        q_ent_gary.H()
        erin.flush()

        print("erin star expansion start")
        star_expansion(q_ent_alice, [q_ent_charlie, q_ent_gary], belongs_W)
        print("erin star expansion end")
        erin.flush()

        charlie_sock.send("go")

    # Print the outcome
    #print(f"erin's outcome with Bob is: {m}")

    # Send the outcome to alice
    #socket.send(str(m))

if __name__ == "__main__":
    main()