# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.compat import is_win, is_linux, is_darwin
import pkginfo

meta_data = pkginfo.get_metadata("flyer_composer")
VERSION = meta_data.version

def Entrypoint(dist, group, name, **kwargs):
    import pkg_resources

    # get toplevel packages of distribution from metadata
    def get_toplevel(dist):
        distribution = pkg_resources.get_distribution(dist)
        if distribution.has_metadata('top_level.txt'):
            return list(distribution.get_metadata('top_level.txt').split())
        else:
            return []

    packages = []
    for distribution in kwargs.get('hiddenimports', []):
        packages += get_toplevel(distribution)

    # get the entry point
    ep = pkg_resources.get_entry_info(dist, group, name)
    # insert path of the egg at the verify front of the search path
    kwargs['pathex'] = [ep.dist.location] + kwargs.get('pathex', [])
    # script name must not be a valid module name to avoid name clashes on import
    script_path = os.path.join(workpath, name + '-script.py')
    print("creating script for entry point", dist, group, name)
    with open(script_path, 'w') as fh:
        print("import", ep.module_name, file=fh)
        print("%s.%s()" % (ep.module_name, '.'.join(ep.attrs)), file=fh)
        for package in packages:
            print("import", package, file=fh)

    return Analysis(
        [script_path] + kwargs.get('scripts', []),
        **kwargs)


a1 = Entrypoint('flyer_composer', 'gui_scripts', 'flyer-composer-gui',
                hookspath=["."],
                excludes=[
                    # saves ~3 MB
                    "PyPDF2.xmp",  # meta-data stuff
                    "pydoc", "doctest", "unittest", "subprocess", "cmd",
                    "bdb", "pickle",
                    "ctypes._aix",
                    #"email", "ftplib", "http.server",
                ])

a2 = Entrypoint('flyer_composer', 'console_scripts', 'flyer-composer',
                hookspath=["."],
                excludes=[
                    # saves ~3 MB
                    "PyPDF2.xmp",  # meta-data stuff
                    "pydoc", "doctest", "unittest", "subprocess", "cmd",
                    "bdb", "pickle",
                    "ctypes",
                ])

pyz1 = PYZ(a1.pure, a1.zipped_data)
pyz2 = PYZ(a2.pure, a2.zipped_data)

def Exe(basename, analysis, pyz, console):
    e = EXE(pyz,
            analysis.scripts,
            [],
            exclude_binaries=True,
            name = basename if not is_win else basename + ".exe",
            strip=False,
            upx=False,
            console=console,
            icon="../artwork/projecticon.ico",
            )
    return e

exe1 = Exe('flyer-composer-gui', a1, pyz1, console=False)
exe2 = Exe('flyer-composer', a2, pyz2, console=True)

coll = COLLECT(exe1, exe2,
               a1.binaries,
               a1.zipfiles,
               a1.datas,
               a2.binaries,
               a2.zipfiles,
               a2.datas,
               strip=False,
               upx=False,
               name='flyer-composer')

if is_win:
    portabel = EXE(pyz1,
                   a1.scripts,
                   a1.binaries,
                   a1.zipfiles,
                   a1.datas,
                   name=os.path.join(os.pardir,
                                     "flyer-composer-%s-portable.exe" % VERSION),
                   strip=False,
                   upx=False,
                   upx_exclude=[],
                   console=False,
                   icon="../artwork/projecticon.ico",
                   )

if is_darwin:
    app = BUNDLE(exe,
                 name='flyer-composer.app',
                 icon=None)
