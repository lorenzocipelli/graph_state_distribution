from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket

def ghz_state_distribution():
    ''' iterate star_expansion() until star graph state is done ''' 


def main(app_config=None, belongs_W=True, other_nodes=[]):
    # lists containing classical and EPR sockets with non-center nodes
    epr_sock = {}

    for element in other_nodes:
        epr_sock[element] = EPRSocket(element)

    alice = NetQASMConnection(
        "alice",
        log_config=app_config.log_config,
        epr_sockets=list(epr_sock.values()),
    )
    with alice:
        # Create an entangled pair using the EPR socket to bob
        q_ent_erin = epr_sock["erin"].recv_keep()[0]
        #m_bob = q_ent_bob.measure()

        #alice.flush()

        # Print the outcome
        #print(f"alice's outcome with Bob is: {m_bob}")

if __name__ == "__main__":
    main()