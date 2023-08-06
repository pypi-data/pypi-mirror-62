"""Training methods for rhasspyfuzzywuzzy"""
import logging
import typing

import networkx as nx
import rhasspynlu

from .const import ExamplesType

_LOGGER = logging.getLogger(__name__)

# -----------------------------------------------------------------------------


def train(graph_dict: typing.Dict[str, typing.Any]) -> ExamplesType:
    """Generate examples from intent graph."""

    # Convert to directed graph
    intent_graph = rhasspynlu.json_to_graph(graph_dict)

    # Generate all possible intents
    _LOGGER.debug("Generating examples")
    examples: ExamplesType = {
        intent_name: {" ".join(words): path}
        for intent_name, words, path in generate_examples(intent_graph)
    }

    _LOGGER.debug("Examples generated")

    return examples


# -----------------------------------------------------------------------------


def generate_examples(
    intent_graph: nx.DiGraph,
) -> typing.Iterable[typing.Tuple[str, typing.List[str], typing.List[int]]]:
    """Generate all possible sentences/paths from an intent graph."""
    n_data = intent_graph.nodes(data=True)

    # Get start/end nodes for graph
    start_node, end_node = rhasspynlu.jsgf_graph.get_start_end_nodes(intent_graph)
    assert (start_node is not None) and (
        end_node is not None
    ), "Missing start/end node(s)"

    # Generate all sentences/paths
    paths = nx.all_simple_paths(intent_graph, start_node, end_node)
    for path in paths:
        assert len(path) > 2

        # First edge has intent name (__label__INTENT)
        olabel = intent_graph.edges[(path[0], path[1])]["olabel"]
        assert olabel.startswith("__label__")
        intent_name = olabel[9:]

        sentence = []
        for node in path:
            word = n_data[node].get("word")
            if word:
                sentence.append(word)

        yield (intent_name, sentence, path)
