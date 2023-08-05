# SOCO-Doc-Parser Python SDK
Python client to use SOCO document parsing platform

## Install 
    pip install soco-doc-parser-python
    
## Quick Start

This following example can be found at: quick_start.py. To see more examples, check out /examples folder

First of all, register at https://app.soco.ai. After get your API_KEYs, you can parse document files 
using 10 lines of code!

```python
from soco_parser.doc_api import DocAPI
from soco_parser.utils import pprint_json


if __name__ == '__main__':
    PARSER_API_KEY = 'convmind'
    client = DocAPI(PARSER_API_KEY)
    """
        parsing a url
    """
    #url = "https://convmind-images.s3.us-east-2.amazonaws.com/pdfview/Fresh_Start_Program_Summary.pdf"
    #parsed_data = client.parse(file_url=url)

    """
        parsing a local file
    """
    parsed_data = client.parse_local_file("resources/1906.09308.pdf",lang="en") #lang="en" or lang="zh"
    pprint_json(parsed_data)
```

## Contact
kyusongl@soco.ai
