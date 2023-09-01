from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket


def main(app_config=None, belongs_W=True, n_names=0, names=[]):

    c_sockets = []
    epr_sockets = []

    # for x in range(n_names) :
    #     # Setup a classical socket to each node
    #     c_sockets.append(Socket("david", names[x], log_config=app_config.log_config))
    #     # Setup an EPR socket to each node
    #     epr_sockets.append(EPRSocket(names[x]))

    epr_sock_alice = EPRSocket("alice")
    epr_sock_bob = EPRSocket("bob")
    epr_sock_charlie = EPRSocket("charlie")

    david = NetQASMConnection(
        "david",
        log_config=app_config.log_config,
        epr_sockets=[epr_sock_alice, epr_sock_bob, epr_sock_charlie],
    )
    with david:
        # Receive an entangled pair using the EPR socket to bob
        q_ent = epr_sock_bob.recv_keep()[0]
        # Measure the qubit
        # m = q_ent.measure()
        print("david ha finito")
    # Print the outcome
    #print(f"david's outcome with Bob is: {m}")


if __name__ == "__main__":
    main()