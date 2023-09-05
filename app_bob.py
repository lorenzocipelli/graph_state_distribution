from netqasm.sdk.external import NetQASMConnection, Socket
from netqasm.sdk import EPRSocket
from star_expansion import star_expansion

def main(app_config=None, belongs_W=True, other_nodes = []):
    epr_sock = {}
    #charlie_sock = Socket("bob", "charlie", log_config=app_config.log_config)

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

        # attendo che charlie abbia finito il suo star expansion
        """ charlie_sock.recv() # sincronizzazione forzata

        print("bob star expansion start")
        star_expansion(q_ent_charlie, [q_ent_frank], belongs_W)
        print("bob star expansion end") """

        #bob.flush()

        '''
            ## VECCHIO CODICE (senza funzioni) ##
            
            print("STAR EXPANSION BEGIN")
            # ----------------------------------------------------
            # abbiamo tre Qubit che sono entrangled con altri nodi
            # ma non sono entangled localmente fra di loro
            q_ent_alice.cphase(q_ent_charlie)
            q_ent_alice.cphase(q_ent_david)
            q_ent_charlie.cphase(q_ent_david)
            # a questo punto i qubit sono entangled localmente
            # se vogliamo fare COMPLEMENTAZIONE LOCALE sappiamo
            # che il qubit a0 è q_ent_alice, questo qubit subisce una rotazione
            # sull'asse X della sfera di -pi/4, mentre gli altri due una rotazione
            # sull'asse Z di pi/4
            q_ent_alice.rot_X(3,2) # 3pi/4 == -pi/4
            q_ent_charlie.rot_Z(1,2)
            q_ent_david.rot_Z(1,2)
            # siccome che il nodo Bob appartiene a W
            # allora non eliminiamo q_ent_alice, ma applichiamo
            # gate CZ per rimuovere tutti i collegamenti interni a bob (ogni combinazione)
            q_ent_alice.cphase(q_ent_charlie)
            q_ent_alice.cphase(q_ent_david)
            q_ent_charlie.cphase(q_ent_david) # NON CREDO VADA FATTO, era già stato eliminato con l'LC
            # a questo punto possiamo effettuare le misurazioni in base Y
            # su tutti gli altri qubit non q_ent_alice
            q_ent_charlie.rot_Z(3,1) # S^dagger, 3pi/2 == -pi/2
            q_ent_charlie.H()
            q_ent_charlie.measure() # Y-basis measurement
            q_ent_david.rot_Z(3,1) # S^dagger, 3pi/2 == -pi/2
            q_ent_david.H()
            q_ent_david.measure() # Y-basis measurement
            # ----------------------------------------------------
            print("STAR EXPANSION END")
        '''

    # m_alice = q_ent_alice.measure()
    # # Print the outcome
    # print(f"bob's outcome with Alice is: {m_alice}")

if __name__ == "__main__":
    main()