from importlib import import_module, resources
import typing as t
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from babu.db import Model
from ruamel.yaml import YAML
import click

@click.command()
@click.argument('import_path')
def cli(import_path):
    main(import_path)

def main(import_path):
    models = load_models(import_path)
    Session = create_db(models)
    session = Session()
    load_data(session, import_path)
    iterbl = build_site(session, import_path)
    publisher = load_publisher(import_path)
    publisher(iterbl)


def load_models(import_path) -> t.Set[Model]:
    # TODO: replace this with a metaclass registry mechanism
    model_path = f'{import_path}.models'
    models_mod = import_module(model_path)
    models_items = models_mod.__dict__.items()
    return {n: o for n, o in models_items if isinstance(o, type) and issubclass(o, Model) and o is not Model}


def create_db(models: t.Set[Model]) -> t.Type[Session]:
    # TODO: replace this with an on-disk DB with change detection of some kind
    engine = create_engine('sqlite:///:memory:')
    Model.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session

yaml = YAML(typ='safe')

def load_data(session: Session, import_path: str, *, prefix=()):
    data_path = '.'.join((import_path, 'data', *prefix))
    for entry in resources.contents(data_path):
        if entry in ('__init__.py', '__pycache__'):
            continue
        if resources.is_resource(data_path, entry):
            # This is a resource (ie a file)
            t = resources.read_text(data_path, entry)
            load_file(session, prefix, entry, t)
        else:
            # This is a directory (so recurse into it)
            load_data(session, import_path, prefix=(*prefix, entry))

def load_file(session: Session, prefix: t.Sequence[str], fullname: str, content: str):
    name, ext = fullname.split('.', 1)
    data = deserialize_file(ext, content)
    cls = Model._decl_class_registry[data['_type']]
    inst = cls()
    inst.id = '.'.join((*prefix, name))
    for k, v in data.items():
        if k == '_type': continue
        setattr(inst, k, v)
    session.add(inst)
    session.commit()

def deserialize_file(ext: str, content: str) -> dict:
    if ext in ('yml', 'yaml'):
        return yaml.load(content)

def build_site(session: Session, import_path: str):
    views_path = f'{import_path}.views'
    views_mod = import_module(views_path)
    root_router = views_mod.app
    return root_router.get_all(session)

def load_publisher(import_path: str):
    mod = import_module(import_path)
    return mod.publisher

if __name__ == "__main__":
    cli()