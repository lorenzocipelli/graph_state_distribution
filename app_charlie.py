from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket


def main(app_config=None, belongs_W=True, n_names=0, names=[]):

    c_sockets = []
    epr_sockets = []

    # for x in range(n_names) :
    #     # Setup a classical socket to each node
    #     c_sockets.append(Socket("charlie", names[x], log_config=app_config.log_config))
    #     # Setup an EPR socket to each node
    #     epr_sockets.append(EPRSocket(names[x]))

    epr_sock_alice = EPRSocket("alice")
    epr_sock_bob = EPRSocket("bob")
    epr_sock_david = EPRSocket("david")

    charlie = NetQASMConnection(
        "charlie",
        log_config=app_config.log_config,
        epr_sockets=[epr_sock_alice, epr_sock_bob, epr_sock_david],
    )
    with charlie:
        # Receive an entangled pair using the EPR socket to bob
        q_ent = epr_sock_bob.recv_keep()[0]

    # Print the outcome
    #print(f"charlie's outcome with Bob is: {m}")

    # Send the outcome to alice
    #socket.send(str(m))

if __name__ == "__main__":
    main()