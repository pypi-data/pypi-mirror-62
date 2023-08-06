"""PEP517 pyproject.toml support. One major restriction: build isolation is not supported"""
import os
import shutil
import tempfile
import importlib

import toml

from .dist_info import _parse_flat_metadata, _fetch_from_wheel


def _create_build_backend(build_system):
    backend_name = build_system["build-backend"]
    module, _, obj = backend_name.partition(":")
    backend = importlib.import_module(module)
    if obj:
        backend = getattr(backend, obj)
    return backend


def _parse_from_prepared_metadata(source_file, backend):
    prepare = getattr(backend, "prepare_metadata_for_build_wheel", None)
    if prepare is None:
        return None

    dest = tempfile.mkdtemp(suffix="metadata")
    old_cwd = os.getcwd()
    try:
        os.chdir(source_file)
        info = prepare(dest)
        meta_info = os.path.join(dest, info, "METADATA")
        if os.path.exists(meta_info):
            with open(meta_info, "r") as file_handle:
                return _parse_flat_metadata(file_handle.read())
    finally:
        shutil.rmtree(dest)
        os.chdir(old_cwd)

    return None


def _parse_from_wheel(backend):
    build_wheel = getattr(backend, "build_wheel", None)
    if build_wheel is None:
        return None
    dest = tempfile.mkdtemp()
    try:
        wheel = build_wheel(dest)
        return _fetch_from_wheel(os.path.join(dest, wheel))
    finally:
        shutil.rmtree(dest)


def fetch_from_pyproject(source_file):
    """Fetch metadata from pyproject.toml either by relying on the backend to provide metadata, or by building
    a wheel and extracting the metadata"""
    try:
        pyproject = toml.load(os.path.join(source_file, "pyproject.toml"))
    except toml.TomlDecodeError:
        return None

    backend = _create_build_backend(pyproject["build-system"])
    result = _parse_from_prepared_metadata(source_file, backend)
    if result is not None:
        return result

    result = _parse_from_wheel(backend)
    return result
