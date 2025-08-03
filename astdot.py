import ast
import inspect

STY = '''
node [fontname="JetBrains Mono" fontsize=15 style=filled
      fillcolor="#E5FDCD" penwidth=1.5]
edge [fontname="JetBrains Mono" fontsize=12 fontcolor="#555555"]
'''.rstrip()


def graph_to_dot(graph, node_labels, edge_labels, style):
    dot = [f'digraph {{{style}']
    for n in graph:
        dot.append(f'{n} [label="{node_labels[n]}" shape=box]')
    for src in graph:
        for dst in graph[src]:
            dot.append(f'{src} -> {dst} [label="{edge_labels[(src, dst)]}"]')
    dot.append('}')
    return '\n'.join(dot)


def skip(name, value):
    return name != 'value' and value in ([], None)


def ast_to_dot(node, skip=skip, style=STY):
    def walk_fields(node_id, node):
        args = []
        for name, value in ast.iter_fields(node):
            match value:
                case _ if skip(name, value):
                    pass
                case ast.AST() | list():
                    walk_node(node_id, value, f'.{name}')
                case _:
                    args.append(f'{name}: {repr(value)}')
        return args

    def walk_node(parent_id, node, edge_label):
        node_id = len(graph)
        graph[node_id] = []
        if parent_id is not None:
            graph[parent_id].append(node_id)
            edge_labels[(parent_id, node_id)] = edge_label
        match node:
            case ast.AST():
                args = [node.__class__.__name__] + walk_fields(node_id, node)
                node_labels[node_id] = '\\n'.join(args)
            case list():
                node_labels[node_id] = 'list'
                for i, x in enumerate(node):
                    walk_node(node_id, x, f'[{i}]')

    graph, node_labels, edge_labels = {}, {}, {}
    walk_node(None, node, '')
    return graph_to_dot(graph, node_labels, edge_labels, style)


def source_to_dot(source, skip=skip, style=STY):
    return ast_to_dot(ast.parse(source), skip, style)


def object_to_dot(obj, skip=skip, style=STY):
    return source_to_dot(inspect.getsource(obj), skip, style)
