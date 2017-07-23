import ast
import sys
import pathlib

import mccabe


def collect_sources():
    top_path = pathlib.Path(".")
    for py_path in top_path.glob("**/*.py"):
        yield py_path


def process(py_source, max_complexity):
    code = py_source.read_text()
    tree = compile(code, py_source, "exec", ast.PyCF_ONLY_AST)
    visitor = mccabe.PathGraphingAstVisitor()
    visitor.preorder(tree, visitor)
    for graph in visitor.graphs.values():
        if graph.complexity() > max_complexity:
            text = "{}:{}:{} {} {}"
            return text.format(py_source, graph.lineno, graph.column,
                               graph.entity, graph.complexity())


def main():
    max_complexity = int(sys.argv[1])
    ok = True
    for py_source in collect_sources():
        error = process(py_source, max_complexity)
        if error:
            ok = False
            print(error)
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
