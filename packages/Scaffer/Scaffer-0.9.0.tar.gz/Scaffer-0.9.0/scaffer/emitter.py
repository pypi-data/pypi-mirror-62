from __future__ import print_function

import os
import re
import itertools
from pprint import pprint
import contextlib
from typing import List, Tuple, Sequence


@contextlib.contextmanager
def remember_cwd():
    curdir= os.getcwd()
    try: yield
    finally: os.chdir(curdir)

def is_binary_content(cont: bytes):
    return b'\0' in cont

def discover_variables(cont: str):
    locase_spans = re.findall(r"scf[\.\-\_\:]?([a-z]+)", cont)
    upcase_spans = list((u.lower() for u in re.findall(r"SCF[\.\-\_]?([A-Z]+)", cont)))
    pascalcase_spans = list((u.lower() for u in re.findall(r"Scf([A-Z][a-z]+)", cont)))

    return set(locase_spans + upcase_spans + pascalcase_spans)


def get_renderings(var_name: str, var_value: str) -> List[Tuple[bytes, bytes]]:
    parts = var_value.split("-")
    
    return [(a.encode(), b.encode()) for a,b in 
        [
        ("scf." + var_name, ".".join(parts)),
        ("scf-" + var_name, "-".join(parts)),
        ("scf_" + var_name, "_".join(parts)),
        #special verbatim syntax
        ("scf:" + var_name, var_value),
        ("Scf" + var_name.title(), "".join(p.title() for p in parts)),
        ("scf" + var_name, "".join(parts)),
        ("SCF" + var_name.upper(), "".join(parts).upper())
        ]]


def apply_replacements(cont: bytes, replacements: List[Tuple[bytes,bytes]]):
    if is_binary_content(cont):
        return cont
    for (fr,to) in replacements:
        cont = cont.replace(fr, to)
    return cont

def rendered_content(template, replacements):
    return [
        (apply_replacements(fname, replacements), apply_replacements(content, replacements)) for (fname, content) in template
    ]

def prompt_variables(vars):
    d = {}
    print("Will need variables:", ", ".join(vars))
    print("Use kebab-case. E.g. if you want MyClass, enter 'my-class'.")
    for v in vars:
        val = input("%s: " % v)
        d[v] = val.strip()
    return d

def var_renderings(d):
    r =  list(itertools.chain(*[get_renderings(k,v) for (k,v) in d.items()]))
    return r

def files_with_content(rootdir) -> Sequence[Tuple[bytes, bytes]]:
    """ -> (fname, content)[] """
    for dirpath, _, fnames in os.walk(rootdir):
        if ".git" in dirpath:
            continue
        for f in fnames:
            # reserved namespace
            if f.startswith("scaffer_"):
                continue
            dp = os.path.join(dirpath, f)
            yield (dp.encode(), open(dp,"rb").read())

def run_scaffer_init(pth, vars, prefilled, target_dir):
    """ Run scaffer_init.py.

    This is run in target dir!
     """
    print("Running", pth)
    cont=  open(pth).read()
    output_dict = {}
    ns = {
        "scaffer_in": {
            "vars": vars,
            "prefilled": prefilled
        },
        # the populated vars should end up here
        "scaffer_out": output_dict
    }
    with remember_cwd():
        os.chdir(target_dir)
        exec(cont, ns)

    if output_dict:
        print("Variables from scaffer_init.py:")
        pprint(output_dict)
        prefilled.update(output_dict)

