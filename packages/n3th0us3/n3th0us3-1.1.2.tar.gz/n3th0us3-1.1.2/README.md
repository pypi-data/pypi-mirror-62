# N3th0us3

**N3th0us3** is unofficial python package for _domains.nethouse.ru/domains_ service.

## Description

Service _domains.nethouse.ru/domains_ lets you check domain name across multiple top-level domains (citation: "checking the domain for occupancy, check whether the domain is occupied in all zones").

But this checking is sequential, one by one. Ohhh...

**N3th0us3**:
 - implements domain name checking function
 - lets to make it faster with multiprocess usage, not sequential
 - lets to make it at a time for multiple domains names
 - gives you interface for python

You can use **N3th0us3** for print result data in console or saving it at file or database.
Just realize this business logic at your callback function.

## Install

```bash
$ pip install n3th0us3
```

## Example

Native usage:

```python
from n3th0us3 import pooled_domains_info

def your_callback_for_each_sub_request(data):
    print(data)
    
if __name__ == '__main__':
        
    pooled_domains_info(
        ['first-domain', 'second-domain',], 
        processes_count=16,
        callback_method=your_callback_for_each_sub_request
    )
```

or low-level usage of **N3th0us3** in your script with command line usage:

```bash
python3 your_script.py first-domain second-domain third-domain -p 10 -tld ru su com
```

```python
# file: your_script.py

import multiprocessing

from n3th0us3.domains import (
    TLD,
    formatted_print,
    get_domain_info
)

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("domain_name",
                        nargs='+',
                        help="space separated domains names list")
    parser.add_argument("-p", dest="processes_count", default=4,
                        type=int,
                        help="count of processes")
    parser.add_argument("-tld", dest="tld",
                        nargs='+', default=TLD,
                        help="space separated top-level domains")

    args = parser.parse_args()

    pool = multiprocessing.Pool(processes=args.processes_count)

    for domain_name in args.domain_name:
        for tld in args.tld:
            pool.apply_async(get_domain_info, args=(domain_name, tld), callback=formatted_print)

    pool.close()
    pool.join()
```
result is:
```text
third-domain.su {'result': {'error': 'empty', 'domain': 'third-domain.su', 'errrr': '', 'is_premium_name': '', 'premium_price': ''}}
third-domain.com {'result': {'error': 'empty', 'domain': 'third-domain.com', 'errrr': '', 'is_premium_name': '', 'premium_price': ''}}
first-domain.com {'result': {'error': 'occupy', 'domain': 'first-domain.com', 'errrr': '', 'error_message': 'Домен занят', 'type_error': 'busy'}}
first-domain.su {'result': {'error': 'empty', 'domain': 'first-domain.su', 'errrr': '', 'is_premium_name': '', 'premium_price': ''}}
third-domain.ru {'result': {'error': 'empty', 'domain': 'third-domain.ru', 'errrr': '', 'is_premium_name': '', 'premium_price': ''}}
second-domain.com {'result': {'error': 'occupy', 'domain': 'second-domain.com', 'errrr': '', 'error_message': 'Домен занят', 'type_error': 'busy'}}
first-domain.ru {'result': {'error': 'empty', 'domain': 'first-domain.ru', 'errrr': '', 'is_premium_name': '', 'premium_price': ''}}
second-domain.ru {'result': {'error': 'empty', 'domain': 'second-domain.ru', 'errrr': '', 'is_premium_name': '', 'premium_price': ''}}
second-domain.su {'result': {'error': 'empty', 'domain': 'second-domain.su', 'errrr': '', 'is_premium_name': '', 'premium_price': ''}}
```

## To be continue...