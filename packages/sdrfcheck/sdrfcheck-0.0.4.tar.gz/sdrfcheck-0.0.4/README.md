# sdrfcheck

Library and tool to validate an sdrf (Sample and Data Relationship Format) for proteomics. The file format specification can be found here
(https://github.com/bigbio/proteomics-metadata-standard)


# How to use it:

First you need to install the tool:

```bash
pip install sdrfchecker
```

Then, you can use the tool by executing the following command:

```bash
python sdrfchecker.py validate-sdrf --sdrf_file {here_the_path_to_sdrf_file}
```

