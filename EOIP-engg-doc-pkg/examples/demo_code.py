# Synthetic demo code used by the documented MVP fixture.

def compute_impact(graph, symbol_id, max_depth=4):
    """Return bounded dependency impact for a canonical code symbol."""
    return graph.impact(symbol_id=symbol_id, max_depth=max_depth)
