import os
import argparse
from pprint import pprint


this_dir = os.getcwd()
JUST_PRINT = True

class InvalidTargetError(Exception):
    pass

# ====== WRAPPERS FOR MOVE, LINK, DELETE =======================================

def check_file(file):
    if os.path.exists(file) and not os.path.islink(file):
        raise ExistsAndNotLinkError(file)

def move_wrapper(src, dst):
    check_file(src)
    check_file(dst)
    if JUST_PRINT:
        print("move_wrapper({}, {})".format(src, dst))
    else:
        os.rename(src, dst)

def link_wrapper(target, link_name):
    check_file(target)
    check_file(link_name)
    if JUST_PRINT:
        print("link_wrapper({}, {})".format(target, link_name))
    else:
        os.link(target, link_name)

def delete_wrapper(target):
    check_file(target)
    if JUST_PRINT:
        print("delete_wrapper({})".format(target))
    else:
        os.remove(target)

# ===== OPERATIONS ON FILES ====================================================

def make_restore_filename(original):
    return os.path.join(this_dir, os.path.basename(original) + '.restore')

def save_target(target, my_file=None):
    backup = make_restore_filename(target)
    move_wrapper(target, backup)

def restore_target(target):
    if os.path.exists(target):
        delete_wrapper(target)

    backup = make_restore_filename(target)
    if os.path.exists(backup):
        move_wrapper(backup, target)

def delete_backups():
    # restore_files=$(find . -name '.*.restore' -o -name '*.restore')
    # rm -f *.restore .*.restore
    pass

def maybe_link(target, link_name):
    if os.path.exists(target):
        link_wrapper(target, link_name)

def unlink_target(target):
    delete_wrapper(target)

def save_and_link(target, my_file):
    save_target(target, my_file)
    maybe_link(my_file, target)

def status(target, my_file):
    pass

# ===== READ LINKFILE AND VALIDATION ===========================================

def has_groups(linkfile_text):
    pass

def read_linkfile():
    filename = os.path.join(this_dir, 'Linkfile')

    data = read_config_file(filename)

class ConfigFileError(Exception):
    pass

def read_config_file(filename):
    data = {}
    lines = []
    current_group = None

    with open(filename) as f:
        lines = map(lambda s : s.strip(), f.readlines())

    line_number = 0
    for l in lines:
        line_number += 1
        words = l.split()
        if words[0].startswith('#'):
            continue
        if words[0].startswith('['):
            current_group_name = words[0].strip('[]')
            current_group = []
            data[current_group_name] = current_group
            continue

        try:
            current_group.append({'link':words[0], 'target':words[1]})
        except KeyError:
            raise ConfigFileError("Expected group before line {} '{}'".format(line_number, l))


    return data

# ===== COMMAND LINE ARGUMENT PARSING ==========================================


if __name__ == "__main__":
    # save_target('/Users/pcarphin/.bashrc')
    # save_target('/Users/pcarphin/.piss-bucket')
    # save_target('/Users/pcarphin/.DS_Store')


    dat = read_config_file("/Users/pcarphin/.philconfig/Linkfile")
    pprint(dat)
    # read_linkfile()
