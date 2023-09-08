from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from star_expansion import star_expansion, QubitSocket

def main(app_config=None, belongs_W=True, other_nodes = []):
    epr_sock = {}
    alice_sock = Socket("bob", "alice", log_config=app_config.log_config)
    charlie_sock = Socket("bob", "charlie", log_config=app_config.log_config)
    frank_sock = Socket("bob", "frank", log_config=app_config.log_config)

    for element in other_nodes:
        epr_sock[element] = EPRSocket(element)

    bob = NetQASMConnection(
        "bob",
        log_config=app_config.log_config,
        epr_sockets=list(epr_sock.values()),
    )
    with bob:      
        q_ent_charlie = epr_sock["charlie"].create_keep()[0]
        q_ent_charlie.H()
        
        q_ent_frank = epr_sock["frank"].create_keep()[0]
        q_ent_frank.H()

        bob.flush()

        msg = charlie_sock.recv()
        while (msg == "rot_Z") :
            q_ent_charlie.rot_Z(1,2) # pi/4
            bob.flush()
            charlie_sock.send("done_rot_Z")
            msg = charlie_sock.recv()

        # attendo che charlie abbia finito il suo star expansion
        charlie_sock.recv() # sincronizzazione forzata

        # creazione oggetti in vista dello Star Expansion
        # notare che la socket classica di Charlie viene rimpiazzata con quella di Alice
        # questo perché dopo il secondo SE Bob comunicherà direttamente con il centro
        # stella, ovvero proprio con Alice
        qs_charlie = QubitSocket(local_qubit=q_ent_charlie, classic_socket=alice_sock)
        qs_frank = QubitSocket(local_qubit=q_ent_frank, classic_socket=frank_sock)

        print("Bob: star expansion start")
        star_expansion(a_0_qubit_socket=qs_charlie,
                c_i_qubit_socket=[qs_frank],
                belongs_W=belongs_W, 
                conn=bob)
        print("Bob: star expansion end")

if __name__ == "__main__":
    main()