# meow
A simple, fast and powerful enterprise email finder tool was built by antx, which based on pocx.

## Description
Meow is a simple, fast and powerful enterprise email finder tool was built by antx, which based on pocx. Meow support search engine and some 
email related websites to find enterprise email. The support engine and site list as follows:

### Search Engine
- Ask
- Baidu
- Bing
- Google
- Qwant
- So
- Sougou

### Email Related Websites
- Email Format
- Have I Been Pwned
- Hunter
- Pgp
- SkyMem

## Install

```bash
git clone https://github.com/antx-code/meow.git
```
## Install Dependencies
```shell
poetry install
```

## Usage
When you use meow to collect more useful information, you can set config into config.yaml.

### Meow Sample:

#### command line sample:

```shell
python3 meow.py target.com
```

#### python3 lib sample:

```python
# Title: xxxxxxx
# Author: antx
# Email: wkaifeng2007@163.com

from meow import dia

if __name__ == '__main__':
    dia('target.com')
```