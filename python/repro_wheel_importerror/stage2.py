def printcache():
    import sys
    print('\n'.join(sorted(sys.path_importer_cache)))

def main():
    # 1) Bootstrap the install system; setuptools and pip are already installed, just need wheel
    import sys
    from subprocess import check_call
    check_call((sys.executable, '-m', 'pip.__main__', 'install', 'wheel'))

    printcache()

    pathfinder = sys.meta_path[-1]

    import distutils.sysconfig
    site_packages = distutils.sysconfig.get_python_lib()
    filefinder = pathfinder._path_importer_cache(site_packages)

    print('site-packages cache:', filefinder._path_cache)

    try:
        import wheel
        print('WHEEL(1):', wheel)
    except ImportError:
        import pdb
        pdb.set_trace()

    filefinder._fill_cache()
    import wheel
    print('WHEEL(2):', wheel)


demo = '''
(Pdb) sys.path_importer_cache['/private/var/folders/ss/ykf37pld1hl480qcdknf_zc577t9rc/T/pytest-163/test_noop_install_faster4/virtualenv_run/lib/python3.4/site-packages']._path_cache
{'_markerlib', 'pip', 'setuptools', 'pip-1.5.6.dist-info', 'setuptools-3.6.dist-info', '__pycache__', 'pkg_resources.py', 'easy_install.py'}

(Pdb) sys.path_importer_cache['/private/var/folders/ss/ykf37pld1hl480qcdknf_zc577t9rc/T/pytest-163/test_noop_install_faster4/virtualenv_run/lib/python3.4/site-packages']._fill_cache()
(Pdb) sys.path_importer_cache['/private/var/folders/ss/ykf37pld1hl480qcdknf_zc577t9rc/T/pytest-163/test_noop_install_faster4/virtualenv_run/lib/python3.4/site-packages']._path_cache
{'wheel', 'wheel-0.24.0.dist-info', '_markerlib', 'pip', 'setuptools', 'pip-1.5.6.dist-info', 'setuptools-3.6.dist-info', '__pycache__', 'pkg_resources.py', 'easy_install.py'}
'''

if __name__ == '__main__':
    exit(main())
