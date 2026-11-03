"""Valida que todos los YAML de k8s/ e infra/ parseen (tags de CloudFormation incluidos)."""
import pathlib
import sys

import yaml


class Loader(yaml.SafeLoader):
    pass


def _any(loader, suffix, node):
    if isinstance(node, yaml.ScalarNode):
        return loader.construct_scalar(node)
    if isinstance(node, yaml.SequenceNode):
        return loader.construct_sequence(node)
    return loader.construct_mapping(node)


Loader.add_multi_constructor("!", _any)

root = pathlib.Path(__file__).resolve().parent.parent
errors = 0
for path in sorted(list(root.glob("k8s/*.y*ml")) + list(root.glob("infra/*.y*ml")) + [root / "buildspec.yml"]):
    try:
        list(yaml.load_all(path.read_text(encoding="utf-8"), Loader=Loader))
        print(f"OK   {path.relative_to(root)}")
    except yaml.YAMLError as exc:
        errors += 1
        print(f"FAIL {path.relative_to(root)}: {exc}")
sys.exit(1 if errors else 0)
