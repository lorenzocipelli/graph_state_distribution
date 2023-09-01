from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket


def main(app_config=None, belongs_W=True, other_nodes=[]):
    
    epr_sock = {}

    for element in other_nodes:
        epr_sock[element] = EPRSocket(element)
   
    frank = NetQASMConnection(
        "frank",
        log_config=app_config.log_config,
        epr_sockets= list(epr_sock.values()),
    )
    with frank:
        # Receive an entangled pair using the EPR socket to bob
        q_ent = epr_sock["bob"].recv_keep()[0]
        frank.flush()
    # Print the outcome
    #print(f"frank's outcome with Bob is: {m}")

    # Send the outcome to alice
    #socket.send(str(m))

if __name__ == "__main__":
    main()