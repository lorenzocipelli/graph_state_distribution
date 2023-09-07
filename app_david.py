from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket


def main(app_config=None, belongs_W=True, other_nodes=[]):

    epr_sock = {}

    for element in other_nodes:
        epr_sock[element] = EPRSocket(element)

    david = NetQASMConnection(
        "david",
        log_config=app_config.log_config,
        epr_sockets=list(epr_sock.values()),
    )
    with david:
        q_ent_charlie = epr_sock["charlie"].create_keep()[0]
        q_ent_charlie.H()

        david.flush()

    # Print the outcome
    #print(f"david's outcome with Bob is: {m}")


if __name__ == "__main__":
    main()