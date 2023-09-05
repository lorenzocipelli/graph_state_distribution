from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket

def main(app_config=None, belongs_W=True, other_nodes=[]):
    # lists containing classical and EPR sockets with non-center nodes
    epr_sock = {}
    erin_sock = Socket("alice", "erin", log_config=app_config.log_config)
    charlie_sock = Socket("alice", "charlie", log_config=app_config.log_config)
    #bob_sock = Socket("alice", "bob", log_config=app_config.log_config)

    for element in other_nodes:
        epr_sock[element] = EPRSocket(element)

    alice = NetQASMConnection(
        "alice",
        log_config=app_config.log_config,
        epr_sockets=list(epr_sock.values()),
    )
    with alice:
        q_ent_erin = epr_sock["erin"].recv_keep()[0]
        q_ent_erin.H()

        alice.flush()

        erin_sock.recv()
        #print("Remote Node which alice is connected to -> " + q_ent_erin.remote_entangled_node)
        q_ent_erin.rot_Z(1,2)

        charlie_sock.recv()
        q_ent_erin.rot_Z(1,2)
        
        # Print the outcome
        #print(f"alice's outcome with Bob is: {m_bob}")

if __name__ == "__main__":
    main()