import setuptools


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='htdfsdk',
    version='0.0.11',
    description='htdf sdk',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='htdf sdk',
    packages=setuptools.find_packages(exclude=["tests"]),
    author='youngqqcn',
    author_email='youngqqcn@163.com',
    url='https://github.com/youngqqcn/htdfsdk',
    classifiers=[
        'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
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
    install_requires=['ecdsa', 'coincurve', 'bech32', "requests"],

)