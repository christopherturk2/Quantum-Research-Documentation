import cirq

# #############################################################################
# ## Surface Code: Logical Qubit Encoder ##
#
# This script defines the quantum circuits for encoding a logical qubit within
# the surface code. The surface code is a topological quantum error correction
# (QEC) code that has a high threshold, making it a leading candidate for
# building a fault-tolerant quantum computer.
#
# Scientific Concepts:
#   - Logical Qubit: A quantum state encoded across multiple physical qubits
#     to protect it from local errors.
#   - Data & Ancilla Qubits: The code uses two types of physical qubits: "data"
#     qubits that hold the logical state and "ancilla" (or "measure") qubits
#     used to detect errors without disturbing the data.
#   - Entanglement: The encoding process involves creating a highly entangled
#     state (a Greenberger–Horne–Zeilinger or GHZ-like state) among the data
#     qubits, which is the basis of the error protection.
#
# This file provides a basic circuit to prepare a logical |0> state for a
# small, distance-2 surface code patch.
# #############################################################################


class SurfaceCodeEncoder:
    """
    Generates circuits to encode logical qubits in a distance-2 surface code.
    This is a simplified version for demonstration.
    """

    def __init__(self, data_qubits, ancilla_qubits):
        """
        Initializes the encoder with the qubit layout.

        Args:
            data_qubits (list[cirq.GridQubit]): Qubits that store the logical state.
            ancilla_qubits (list[cirq.GridQubit]): Qubits used for error checking.
        """
        self.data_qubits = data_qubits
        self.ancilla_qubits = ancilla_qubits
        self.all_qubits = data_qubits + ancilla_qubits
        print(f"[Encoder] Initialized with {len(data_qubits)} data qubits and {len(ancilla_qubits)} ancilla qubits.")


    def create_logical_zero_circuit(self):
        """
        Creates a circuit to prepare the logical |0> state.

        In the surface code, the logical |0> is the state where all X-stabilizers
        have an eigenvalue of +1. This can be prepared by measuring the
        X-stabilizers and post-selecting or correcting. A simpler method shown
        here is to initialize all data qubits to |0>, which is already an
        eigenstate of the X stabilizers.

        Returns:
            cirq.Circuit: The encoding circuit.
        """
        circuit = cirq.Circuit()

        # The logical |0> for the surface code is simply all data qubits in the
        # |0> state. This state is naturally an eigenstate of the X stabilizers.
        # So, the "encoding" is primarily about ensuring the system is in this
        # ground state before the stabilizer checks begin.
        # We can add explicit resets for clarity.
        circuit.append(cirq.reset(q) for q in self.data_qubits)

        print("[Encoder] Created circuit for logical |0> state.")
        return circuit


# --- Example Usage (for direct testing) ---
if __name__ == '__main__':
    # --- Define a small (distance-2) surface code patch layout ---
    # This is a 2x2 grid of data qubits with ancilla qubits in between.
    # D = Data qubit, A = Ancilla qubit
    #
    #   A   D---A---D
    #       |   |   |
    #   D---A---D---A
    #   |   |   |
    #   A---D---A
    #
    data = [cirq.GridQubit(i, j) for i in [0, 1] for j in [0, 1]]
    ancillas = [cirq.GridQubit(0.5, 0.5), cirq.GridQubit(0.5, 1.5), cirq.GridQubit(1.5, 0.5)]

    # Initialize the encoder
    encoder = SurfaceCodeEncoder(data, ancillas)

    # Create the circuit
    logical_zero_circuit = encoder.create_logical_zero_circuit()

    # Print the circuit to visualize it
    print("\n--- Logical |0> Preparation Circuit ---")
    print(logical_zero_circuit)
    print("--------------------------------------")
    print("Note: For the logical |0>, the circuit is trivial (resets).")
    print("The complex operations occur during the stabilizer measurements.")
