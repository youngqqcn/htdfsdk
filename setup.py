import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='htdfsdk',
    version='1.0.1',
    description='htdf python sdk',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='htdf sdk',
    py_modules=['htdfsdk'],
    packages=setuptools.find_packages(exclude=["tests"]),
    author='youngqqcn',
    author_email='youngqqcn@gmail.com',
    url='https://github.com/youngqqcn/htdfsdk',
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable'
        # 'Development Status :: 5 - Production/Stable',  # 当前开发进度等级（测试版，正式版等）
        'Intended Audience :: Developers',  # 模块适用人群
        'Topic :: Software Development :: Code Generators',  # 给模块加话题标签
        'License :: OSI Approved :: MIT License',  # 模块的license

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.6',
    install_requires=[
        'ecdsa',
        'coincurve',
        'bech32',
        'requests',

        "eth-abi>=2.0.0b6,<3.0.0",
        "eth-account>=0.5.3,<0.6.0",
        "eth-hash[pycryptodome]>=0.2.0,<1.0.0",
        "eth-typing>=2.0.0,<3.0.0",
        "eth-utils>=1.9.5,<2.0.0",
        "hexbytes>=0.1.0,<1.0.0",
        "ipfshttpclient==0.7.0a1",
        "jsonschema>=3.2.0,<4.0.0",
        "lru-dict>=1.1.6,<2.0.0",
        "protobuf>=3.10.0,<4",
        "pypiwin32>=223;platform_system=='Windows'",
        "requests>=2.16.0,<3.0.0",
        # remove typing_extensions after python_requires>=3.8, see web3._utils.compat
         "typing-extensions>=3.7.4.1,<4;python_version<'3.8'",
        "websockets>=8.1.0,<9.0.0",
    ],

)