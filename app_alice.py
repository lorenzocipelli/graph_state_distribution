from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket

def ghz_state_distribution():
    ''' iterate star_expansion() until star graph state is done ''' 


def main(app_config=None, belongs_W=True, n_names=0, names=[]):
    # lists containing classical and EPR sockets with non-center nodes
    c_sockets = []
    epr_sockets = []
    ent_qubits = []
    local_qubits = []

    # for x in range(n_names) :
    #     # Setup a classical socket to each node
    #     c_sock_temp = Socket("alice", names[x], log_config=app_config.log_config)
    #     c_sockets.append(c_sock_temp)
    #     # Setup an EPR socket to each node
    #     epr_sock_temp = EPRSocket(names[x], epr_socket_id= , remote_epr_socket_id=)
    #     epr_sockets.append(epr_sock_temp)

    epr_sock_bob = EPRSocket("bob")
    epr_sock_charlie = EPRSocket("charlie")
    epr_sock_david = EPRSocket("david")

    alice = NetQASMConnection(
        "alice",
        log_config=app_config.log_config,
        epr_sockets=[epr_sock_bob, epr_sock_charlie, epr_sock_david],
    )
    with alice:
        # Create an entangled pair using the EPR socket to bob
        q_ent_bob = epr_sock_bob.recv_keep()[0]
        #m_bob = q_ent_bob.measure()

        #alice.flush()

        # Print the outcome
        #print(f"alice's outcome with Bob is: {m_bob}")

if __name__ == "__main__":
    main()