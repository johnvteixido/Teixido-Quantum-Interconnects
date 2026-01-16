# =============================================================================
# TEIXIDO QUANTUM VOLUME BENCHMARK (PUBLIC REFERENCE)
# Purpose: Verify CNOT gate reduction using Teixido Coupling Maps.
# License: AGPL-3.0
# =============================================================================

import warnings
from qiskit import transpile
from qiskit.circuit.library import QuantumVolume
from qiskit.transpiler import CouplingMap
import networkx as nx

warnings.filterwarnings('ignore')

def run_gate_audit():
    print("--- TEIXIDO GATE COMPLEXITY AUDIT (N=16) ---")
    n = 16
    
    # 1. Create Standard Map (Line)
    line_edges = [[i, i+1] for i in range(n-1)] + [[i+1, i] for i in range(n-1)]
    map_std = CouplingMap(line_edges)
    
    # 2. Create Teixido Map (Random Degree-4)
    G = nx.random_regular_graph(4, n)
    while not nx.is_connected(G): G = nx.random_regular_graph(4, n)
    teix_edges = list(G.edges()) + [(v,u) for u,v in G.edges()]
    map_teix = CouplingMap(teix_edges)
    
    # 3. Benchmark
    qc = QuantumVolume(n, n, seed=42).decompose()
    
    # Compile
    print("Compiling Standard...")
    qc_std = transpile(qc, coupling_map=map_std, optimization_level=3)
    print("Compiling Teixido...")
    qc_teix = transpile(qc, coupling_map=map_teix, optimization_level=3)
    
    cnot_std = qc_std.count_ops().get('cx', 0)
    cnot_teix = qc_teix.count_ops().get('cx', 0)
    
    print(f"\nRESULTS:")
    print(f"Standard CNOT Count: {cnot_std}")
    print(f"Teixido CNOT Count:  {cnot_teix}")
    print(f"Reduction Factor:    {cnot_std/cnot_teix:.2f}x")

if __name__ == "__main__":
    run_gate_audit()
