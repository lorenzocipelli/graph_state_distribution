from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from star_expansion import star_expansion


def main(app_config=None, belongs_W=True, other_nodes=[]):

    epr_sock = {}
    erin_sock = Socket("charlie", "erin", log_config=app_config.log_config)
    alice_sock = Socket("charlie", "alice", log_config=app_config.log_config)
    #bob_sock = Socket("charlie", "bob", log_config=app_config.log_config)

    for element in other_nodes:
        epr_sock[element] = EPRSocket(element)

    charlie = NetQASMConnection(
        "charlie",
        log_config=app_config.log_config,
        epr_sockets=list(epr_sock.values()),
    )
    with charlie:
        q_ent_bob = epr_sock["bob"].recv_keep()[0]
        q_ent_bob.H()

        q_ent_erin = epr_sock["erin"].recv_keep()[0]
        q_ent_erin.H()

        q_ent_david = epr_sock["david"].recv_keep()[0]
        q_ent_david.H()
        
        # attendo che erin abbia finito il suo star expansion
        erin_sock.recv() # sincronizzazione forzata
        
        print("Charlie: star expansion start")
        q_ent_erin, [q_ent_bob, q_ent_david] = star_expansion(a_0_qubit=q_ent_erin,
                                                              c_i_qubits=[q_ent_bob, q_ent_david],
                                                              belongs_W=belongs_W, 
                                                              center_classic_socket=alice_sock,
                                                              conn=charlie)
        print("Charlie: star expansion end")
        charlie.flush()
        #bob_sock.send("go2")
        

    # Print the outcome
    #print(f"charlie's outcome with Bob is: {m}")

    # Send the outcome to alice
    #socket.send(str(m))

if __name__ == "__main__":
    main()