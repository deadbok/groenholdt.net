'''
Config file for my personal blog.
'''
CONFIG = {
        'AUTHOR': 'Martin Bo Kristensen Grønholdt',
        'SITEURL': 'http://librebook/test',
        'SITENAME': 'Homepage V. 5.1',
        'POSTSPERINDEX': 6,
        'METAPARSERS': ['CategoryMetaParser'],
        'GENERATORS': ['BlogIndexGenerator', 'CategoryIndexGenerator', 'TagCloudGenerator'],
        'CONTENTFILTERS': ['LocalURL']
}
