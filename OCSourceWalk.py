#!/usr/bin/env python


def main():
    from clang.cindex import Config
    Config.set_library_path('.')

    info = "Walk Objective-c source code."

    import argparse
    parser = argparse.ArgumentParser(description=info)
    parser.add_argument("-d", "--dir", help="the dir of sources.", type=str)
    parser.add_argument(
        "-f", "--file", help="the file of source code.", type=str)
    # parser.add_argument(
    #     "-w", "--walker", help="the implement walker name.", type=str)
    args = parser.parse_args()

    if args.dir:
        walkDir(args.dir, None)
    elif args.file:
        waklFile(args.file, None)
    else:
        parser.print_help()


def openCMD(cmd):
    import os
    print "[openCmd]" + cmd
    f = os.popen(cmd)
    res = f.read()
    f.close()
    return res


def error(err):
    print "[ERROR]%s" % (err)
    exit(1)


def walkDir(dir_path, walker):
    print "[Walk Directory] " + dir_path
    import os
    text = openCMD("find " + dir_path + ' -iname "*.[hm]"')
    lines = text.strip("\n").split("\n")
    for line in lines:
        if os.path.isfile(line):
            waklFile(line, walker)
        else:
            error(line + " is not valide file.")


def waklFile(file_path, walker):
    print "[Walk File] " + file_path
    from clang.cindex import Index
    import os
    args = [file_path]
    index = Index.create()
    tu = index.parse(None, args)
    walkTU(tu, file_path , walker)


def walkTU(tu, file_name, walker):
    tu_cursors = tu.cursor.get_children()
    for tc in tu_cursors:
	    walkCursor(tc, file_name, walker)


def walkCursor(cursor, file_name, walker):
    nofileKind = ('OBJC_SYNTHESIZE_DECL')
    if cursor.location.file:
        if cursor.location.file.name == file_name:
            handleWalker(cursor,walker)
            for c in cursor.get_children():
                walkCursor(c, file_name, walker)
    elif cursor.kind.name in nofileKind:
        handleWalker(cursor,walker)
        for c in cursor.get_children():
            walkCursor(c, file_name, walker)
    else:
        print "----cursor has no file.----"
        printCursor(cursor)

def handleWalker(cursor,walker):
    if walker:
        walker.walk(cursor)
    else:
        printCursor(cursor)

def printCursor(node):
    info = {'kind': node.kind,
            'usr': node.get_usr(),
            'spelling': node.spelling,
            'displayname': node.displayname,
            'location': node.location, 'file': node.location.file,
            'extent.start': node.extent.start,
            'extent.end': node.extent.end,
            'is_definition': node.is_definition()}
    from pprint import pprint
    pprint(info)

if __name__ == '__main__':
    main()
