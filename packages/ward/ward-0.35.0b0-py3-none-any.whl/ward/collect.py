import importlib
import importlib.util
import inspect
import os
import pkgutil
from importlib._bootstrap import ModuleSpec
from importlib._bootstrap_external import FileFinder
from pathlib import Path
from typing import Any, Callable, Generator, Iterable, List, Set, Tuple

from ward.errors import CollectionError
from ward.models import WardMeta
from ward.testing import Test, anonymous_tests, is_test_module_name
from ward.util import get_absolute_path

Glob = str


def is_test_module(module: pkgutil.ModuleInfo) -> bool:
    return is_test_module_name(module.name)


def get_module_path(module: pkgutil.ModuleInfo) -> Path:
    return Path(module.module_finder.find_module(module.name).path)


def is_excluded_module(module: pkgutil.ModuleInfo, exclusions: Iterable[Glob]) -> bool:
    return excluded(get_module_path(module), exclusions)


def excluded(path: Path, exclusions: Iterable[Glob]) -> bool:
    """Return True if path matches any of the glob patterns in exclusions. False otherwise."""
    return any(path.match(pattern) for pattern in exclusions)


def remove_excluded_paths(
    paths: Iterable[Path], exclusions: Iterable[Glob]
) -> List[Path]:
    return [p for p in paths if not excluded(p, exclusions)]


def handled_within(module_path: Path, search_paths: Iterable[Path]) -> bool:
    """
    Return True if the module path starts with any of the search paths,
    that is, if any module is contained within any of the search paths
    """
    for search_path in search_paths:
        if search_path.is_dir():
            if search_path in module_path.parents:
                return True
    return False


def get_info_for_modules(
    paths: List[Path], exclude: Tuple[Glob],
) -> Generator[pkgutil.ModuleInfo, None, None]:
    paths = remove_excluded_paths(set(paths), exclude)

    # Handle case where path points directly to modules
    for path in paths:
        if path.is_file() and not handled_within(path, paths):
            spec = importlib.util.spec_from_file_location(path.stem, path)
            try:
                mod = importlib.util.module_from_spec(spec)
            except AttributeError as e:
                msg = f"Path {str(path)} is not a valid Python module."
                raise CollectionError(msg) from e
            yield mod

    # Check for modules at the root of the specified path (or paths)
    for mod in pkgutil.iter_modules([str(p) for p in paths if p.is_dir()]):
        if is_test_module(mod) and not is_excluded_module(mod, exclude):
            yield mod

    # Now check for modules in every subdirectory
    checked_dirs: Set[Path] = set(p for p in paths)
    for p in paths:
        for root, dirs, _ in os.walk(str(p)):
            if excluded(Path(root), exclude):
                continue
            for dir_name in dirs:
                dir_path = Path(root, dir_name)
                # if we have seen this path before, skip it
                if dir_path not in checked_dirs and not excluded(dir_path, exclude):
                    checked_dirs.add(dir_path)
                    for mod in pkgutil.iter_modules([str(dir_path)]):
                        if is_test_module(mod) and not is_excluded_module(mod, exclude):
                            yield mod


def load_modules(modules: Iterable[pkgutil.ModuleInfo]) -> Generator[Any, None, None]:
    for m in modules:
        if hasattr(m, "module_finder"):
            file_finder: FileFinder = m.module_finder
            spec: ModuleSpec = file_finder.find_spec(m.name)
            m = importlib.util.module_from_spec(spec)
        if is_test_module_name(m.__name__):
            m.__loader__.exec_module(m)
            yield m


def get_tests_in_modules(
    modules: Iterable, capture_output: bool = True
) -> Generator[Test, None, None]:
    for mod in modules:
        mod_name = mod.__name__
        mod_path = get_absolute_path(mod)
        anon_tests: List[Callable] = anonymous_tests[mod_path]
        if anon_tests:
            for test_fn in anon_tests:
                meta: WardMeta = getattr(test_fn, "ward_meta")
                yield Test(
                    fn=test_fn,
                    module_name=mod_name,
                    marker=meta.marker,
                    description=meta.description or "",
                    capture_output=capture_output,
                )


def search_generally(
    tests: Iterable[Test], query: str = ""
) -> Generator[Test, None, None]:
    if not query:
        yield from tests

    for test in tests:
        description = test.description or ""
        if (
            query in description
            or query in f"{test.module_name}."
            or query in inspect.getsource(test.fn)
            or query in test.qualified_name
        ):
            yield test
