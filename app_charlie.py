from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from star_expansion import dictionary, update_json, star_expansion, star_expansion_neighbour, QubitSocket


def main(app_config=None, belongs_W=True, other_nodes=[]):

    epr_sock = {}

    david_sock = Socket("charlie", "david", log_config=app_config.log_config)
    erin_sock = Socket("charlie", "erin", log_config=app_config.log_config)
    alice_sock = Socket("charlie", "alice", log_config=app_config.log_config)
    bob_sock = Socket("charlie", "bob", log_config=app_config.log_config)

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

        q_ent_david = epr_sock["david"].recv_keep()[0]
        q_ent_david.H()

        q_ent_erin = epr_sock["erin"].recv_keep()[0]
        q_ent_erin.H()
        
        charlie.flush()

        star_expansion_neighbour(conn=charlie,
                            communicating_socket=erin_sock,
                            qubit_to_rotate=q_ent_erin)

        # attendo che erin abbia finito il suo star expansion
        erin_sock.recv() # sincronizzazione forzata

        # creazione oggetti in vista dello Star Expansion
        qs_bob = QubitSocket(local_qubit=q_ent_bob, classic_socket=bob_sock)
        qs_david = QubitSocket(local_qubit=q_ent_david, classic_socket=david_sock)
        # notare che la socket classica di Erin viene rimpiazzata con quella di Alice
        # questo perché dopo il primo SE Charlie comunicherà direttamente con il centro
        # stella, ovvero proprio con Alice
        qs_erin = QubitSocket(local_qubit=q_ent_erin, classic_socket=alice_sock)

        star_expansion(a_0_qubit_socket=qs_erin,
                        c_i_qubit_socket=[qs_bob, qs_david],
                        belongs_W=belongs_W, 
                        conn=charlie)

        bob_sock.send("go2") # per procedere con lo SE di Bob  

        bob_sock.recv()

        m_erin = q_ent_erin.measure()
    #rw_json("Charlie", m_erin)
    dictionary["charlie"].append(int(m_erin))
    update_json()
    print("Charlie measure -> " + str(m_erin))    
    return {"measured": int(m_erin)}

if __name__ == "__main__":
    main()