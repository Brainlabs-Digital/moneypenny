from distutils.core import setup
setup(
    name='moneypenny',
    packages=['moneypenny'],
    version='0.0.3',
    description='A library for normalizing URL lists and creating Google disavow files.',
    author='Rasool Somji',
    author_email='rasool.somji@distilled.net',
    url='https://github.com/DistilledLtd/moneypenny',
    download_url='https://github.com/DistilledLtd/moneypenny/tarball/0.0.3',
    keywords=['urls', 'disavow'],
    classifiers=[],
    install_requires=[
        'tldextract',
        'url'
    ]
)
