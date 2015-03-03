import os
import progress


def scan_missing_files(index, res_folder):
    num_files = len(index)
    missing = 0
    scanned = 0
    for entry in index:
        scanned += 1
        progress.write("Scanned %6.1d of %6.1d files (%6.1d missing)\r" %
                       (scanned, num_files, missing))
        filename = os.path.join(res_folder, entry.cached_name)
        if not os.path.exists(filename):
            missing += 1
            continue
    progress.clear()
    return missing


def scan_extra_files(index_by_cached_names, res_folder):
    extras = 0
    scanned = 0
    for root, dirs, files in os.walk(res_folder):
        for name in files:
            scanned += 1
            progress.write("Scanned %7.1d files (%7.1d extra)\r" % (scanned, extras))
            parent_folder = os.path.split(root)[1]
            cached_name = "%s/%s" % (parent_folder, name)
            if cached_name not in index_by_cached_names:
                extras += 1
    progress.clear()
    return extras


def diff_cache(index, res_folder):
    index_by_cached_names = {}
    for entry in index:
        index_by_cached_names[entry.cached_name] = entry

    extras = scan_extra_files(index_by_cached_names, res_folder)
    missing = scan_missing_files(index, res_folder)

    print "  %6.1d files not yet downloaded" % missing
    print "  %6.1d extra files in cache folder" % extras