# Distributing Graph State over arbitrary Quantum Networks
Every theoretical aspect of our work must be attributed to the work of the authors of the paper: 
* **Clément Meignant** *(1)*
* **Damian Markham** *(1)*
* **Frédéric Grosshans** *(2)*

*(1) Laboratoire d’Informatique de Paris 6, CNRS, Sorbonne Université, 4 place Jussieu, 75005 Paris, France*

*(2) Laboratoire Aimé Cotton, CNRS, Univ. Paris-Sud, ENS Cachan, Univ. Paris-Saclay, 91405 Orsay Cedex*

The paper in question is the following: https://arxiv.org/abs/1811.05445

This protocol implements the task of distributing arbitrary graph states over quantum networks of arbitrary topology. The goal is to distribute this states in a way that is most efficient in terms of the number of Bell pairs consumed and the number of operations realized by the protocol. 
Assumptions:
1) Perfect distribution of Bell pairs occurring at perfectly synchronized times.
2) Perfect node local computation.
3) Ignore the cost of classical communications.
4) Ignore processing time of local quantum processor.
5) Ignore the cost of quantum memory.

To create this project, the **NetQasm** instruction set architecture was used, which allows interfacing with
quantum network controllers and run applications on quantum networks, supporting quantum gates.
Furthermore, NetQasm enables tight integration of classical logic and level communication
application with quantum operations at the physical level. This enables applications of a quantum network
to be programmed in high-level platform-independent software, which is not achievable with
other QASM (Quantum Assembly Language) variants. To take advantage of this architecture, both *assemblies* and, as in
our case, *Python*.

## Initial Graph State
Our net was initiated in a "fixed" way, by choosing the topology in advance, following the structure which was highlighted in the paper.

![init_graph](/images/graph_init.png "Graph initial state")

## Graphical Tools
Following the graphical tools that were described in the paper:
* **Vertex deletion**: this operation removes one vertex and all the associated edges from the graph. Physically, it is implemented by the Pauli measurement of the relevant
qubit in the Z basis.
* **Local complementation** on a vertex: this graph operation inverts the sub-graph induced by the neighborhood
*N_a* of the concerned vertex *a*—the set of vertices adjacent to *a*.
* **Edge addition (deletion)**: by applying a controlled-Z
operation between two qubits belonging to the same
node, we create (delete) an edge between two non-adjacent (adjacent) vertices.

The operations just mentioned are an integral part of the implementation for the next operation, the Star Expansion operation, key element for the realization of the objective defined by the paper.

* **Star Expansion**: The star expansion subprotocol will help us to share the star graph state across the full
 

## Step-by-step
After applying the Star Expansion on Erin we get the follwing topology:

![graph_1](/images/graph_1.png "Graph After Erin SE")

Then we apply the SE to Charlie

![graph_2](/images/graph_2.png "Graph After Charlie SE")

In the end we apply the SE to Bob

![graph_3](/images/graph_3.png "Graph After Bob SE")

Seen that our initial graph state is a GHZ what we would expect to receive is something like this:

![ghz_final](/images/ghz_final.png "Final GHZ state")
