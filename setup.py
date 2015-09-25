from distutils.core import setup
setup(
    name='moneypenny',
    packages=['moneypenny'],
    version='0.0.1',
    description='A library for normalizing URL lists and creating disavow files.',
    author='Rasool Somji',
    author_email='rasool.somji@distilled.net',
    url='https://github.com/DistilledLtd/moneypenny',
    download_url='https://github.com/DistilledLtd/moneypenny/tarball/0.0.1',
    keywords=['urls', 'disavow'],
    classifiers=[],
    install_requires=[
        'tldextract'
    ]
)
