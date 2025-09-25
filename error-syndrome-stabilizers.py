import cirq

# #############################################################################
# ## Surface Code: Stabilizer Measurement Circuits ##
#
# This is the core of the error detection mechanism. Stabilizer circuits are
# run repeatedly to check for errors without measuring (and thus collapsing)
# the logical state of the data qubits.
#
# Scientific Concepts:
#   - Stabilizer Formalism: A method of describing a quantum state not by its
#     state vector, but by the set of operators (stabilizers) of which it is a
#     +1 eigenstate.
#   - Parity Checks: Each stabilizer measurement checks the "parity" of the
#     surrounding data qubits. For an X-stabilizer, it checks if the number of
#     data qubits in the |1> state is even or odd.
#   - Error Syndrome: A non-trivial measurement result from an ancilla qubit
#     (e.g., measuring |1> when |0> was expected) indicates that an error has
#     occurred on an adjacent data qubit. The pattern of these "flipped" ancilla
#     bits is the error syndrome. 
#
# #############################################################################


class StabilizerCircuits:
    """
    Generates stabilizer measurement circuits for a surface code patch.
    """

    def __init__(self, data_qubits, ancilla_qubits):
        """
        Initializes the stabilizer generator.

        Args:
            data_qubits (list[cirq.GridQubit]): Qubits that store the logical state.
            ancilla_qubits (list[cirq.GridQubit]): Qubits used for error checking.
        """
        self.data_qubits = data_qubits
        self.ancilla_qubits = ancilla_qubits
        self.qubit_map = {q: (q.row, q.col) for q in data_qubits + ancilla_qubits}
        print(f"[Stabilizers] Initialized for a {len(data_qubits)} data qubit patch.")


    def _get_neighbors(self, ancilla_qubit):
        """Helper to find the 4 adjacent data qubits for a given ancilla."""
        r, c = self.qubit_map[ancilla_qubit]
        neighbors = []
        # Find qubits at corners relative to the ancilla
        for dr in [-0.5, 0.5]:
            for dc in [-0.5, 0.5]:
                neighbor_pos = (r + dr, c + dc)
                for q, pos in self.qubit_map.items():
                    if pos == neighbor_pos:
                        neighbors.append(q)
        return neighbors

    def create_stabilizer_cycle(self):
        """
        Creates one full cycle of stabilizer measurements (both X and Z type).
        In a real experiment, this cycle is run continuously.
        
        Returns:
            cirq.Circuit: The circuit for one round of error detection.
        """
        circuit = cirq.Circuit()

        # In a real implementation, X and Z stabilizers might be measured in parallel
        # or in alternating rounds. We will build them sequentially for clarity.

        # --- X-Type Stabilizer Measurement (Detects Z-errors/phase-flips) ---
        # 1. Prepare ancilla in |+> state
        circuit.append(cirq.H(ancilla) for ancilla in self.ancilla_qubits)
        # 2. Apply CNOTs from ancilla to neighboring data qubits
        for ancilla in self.ancilla_qubits:
            neighbors = self._get_neighbors(ancilla)
            circuit.append(cirq.CNOT(ancilla, data) for data in neighbors)
        # 3. Bring ancilla out of |+> basis to measure
        circuit.append(cirq.H(ancilla) for ancilla in self.ancilla_qubits)

        # --- Z-Type Stabilizer Measurement (Detects X-errors/bit-flips) ---
        # This would require a separate set of ancillas, which we'll reuse for simplicity.
        # 1. Prepare ancilla in |0> state (already done by measurement reset)
        # 2. Apply CNOTs from data qubits to ancilla
        for ancilla in self.ancilla_qubits:
            neighbors = self._get_neighbors(ancilla)
            circuit.append(cirq.CNOT(data, ancilla) for data in neighbors)

        # --- Final Measurement ---
        # The key is to only measure the ancilla qubits.
        circuit.append(cirq.measure(*self.ancilla_qubits, key='syndrome'))

        print("[Stabilizers] Created one full stabilizer measurement cycle circuit.")
        return circuit


# --- Example Usage (for direct testing) ---
if __name__ == '__main__':
    # Define the same small surface code patch
    data = [cirq.GridQubit(i, j) for i in [0, 1] for j in [0, 1]]
    ancillas = [cirq.GridQubit(0.5, 0.5), cirq.GridQubit(0.5, 1.5), cirq.GridQubit(1.5, 0.5)]

    # Initialize the stabilizer generator
    stabilizer_gen = StabilizerCircuits(data, ancillas)

    # Create the circuit for one cycle
    stabilizer_circuit = stabilizer_gen.create_stabilizer_cycle()

    # Print the circuit
    print("\n--- One Cycle of Stabilizer Measurements ---")
    print(stabilizer_circuit)
    print("--------------------------------------------")
