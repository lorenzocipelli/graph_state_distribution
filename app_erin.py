from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from pprint import pprint
from star_expansion import star_expansion, QubitSocket, label


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
        qs_alice = QubitSocket(local_qubit=q_ent_alice, classic_socket=alice_sock, neighbour_name="alice")
        qs_charlie = QubitSocket(local_qubit=q_ent_charlie, classic_socket=charlie_sock, neighbour_name="charlie")
        qs_gary = QubitSocket(local_qubit=q_ent_gary, classic_socket=gary_sock, neighbour_name="gary")

        star_expansion(a_0_qubit_socket=qs_alice,
                        c_i_qubit_socket=[qs_charlie, qs_gary],
                        belongs_W=belongs_W,
                        neighbour_list=["alice", "charlie", "gary"],
                        ex_star_node="erin",
                        conn=erin)

        pprint(label)
        charlie_sock.send("go1") # per procedere con lo SE di Charlie  

if __name__ == "__main__":
    main()