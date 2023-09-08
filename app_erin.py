from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from star_expansion import star_expansion, QubitSocket


def main(app_config=None, belongs_W=True, other_nodes=[]):

    epr_sock = {}
    gary_sock = Socket("erin", "gary", log_config=app_config.log_config)
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
        q_ent_alice = epr_sock["alice"].create_keep()[0]
        q_ent_alice.H()

        q_ent_charlie = epr_sock["charlie"].create_keep()[0]
        q_ent_charlie.H()
        
        q_ent_gary = epr_sock["gary"].create_keep()[0]
        q_ent_gary.H()

        erin.flush()

        # creazione oggetti in vista dello Star Expansion
        qs_alice = QubitSocket(local_qubit=q_ent_alice, classic_socket=alice_sock)
        qs_charlie = QubitSocket(local_qubit=q_ent_charlie, classic_socket=charlie_sock)
        qs_gary = QubitSocket(local_qubit=q_ent_gary, classic_socket=gary_sock)

        print("Erin: star expansion start")
        star_expansion(a_0_qubit_socket=qs_alice,
                        c_i_qubit_socket=[qs_charlie, qs_gary],
                        belongs_W=belongs_W, 
                        conn=erin)
        print("Erin: star expansion end")
        erin.flush()

        charlie_sock.send("go1") # per procedere con lo SE di Charlie  

if __name__ == "__main__":
    main()