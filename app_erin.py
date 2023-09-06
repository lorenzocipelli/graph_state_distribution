from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from star_expansion import star_expansion


def main(app_config=None, belongs_W=True, other_nodes=[]):

    epr_sock = {}
    charlie_sock = Socket("erin", "charlie", log_config=app_config.log_config)
    alice_sock = Socket("erin", "alice", log_config=app_config.log_config)

    for element in other_nodes:
        epr_sock[element] = EPRSocket(element)

    erin = NetQASMConnection(
        "erin",
        log_config=app_config.log_config,
        epr_sockets=list(epr_sock.values()),
    )
    with erin:
        q_ent_charlie = epr_sock["charlie"].create_keep()[0]
        q_ent_charlie.H()

        q_ent_alice = epr_sock["alice"].create_keep()[0]
        q_ent_alice.H()
        
        q_ent_gary = epr_sock["gary"].create_keep()[0]
        q_ent_gary.H()

        print("Erin: star expansion start")
        q_ent_alice, [q_ent_charlie, q_ent_gary] = star_expansion(a_0_qubit=q_ent_alice,
                                                                  c_i_qubits=[q_ent_charlie, q_ent_gary],
                                                                  belongs_W=belongs_W, 
                                                                  center_classic_socket=alice_sock,
                                                                  conn=erin)
        print("Erin: star expansion end")
        
        erin.flush()
        charlie_sock.send("go1")

    # Print the outcome
    #print(f"erin's outcome with Bob is: {m}")

    # Send the outcome to alice
    #socket.send(str(m))

if __name__ == "__main__":
    main()