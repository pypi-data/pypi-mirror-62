# The Alert Logic SDK For Python (almdrlib)
Alert Logic Software Development Kit for Python allows developers to integrate with Alert Logic MDR Services.

## Quick Start
1. Install the library:

	```$ pip install alertlogic-sdk-python```

2. Set up configuration file (in e.g. ```~/.alertlogic/config```

	```
	[default]
	access_key_id = YOUR_KEY
	secret_key = YOUR_SECRET
	```

	Optionally you can specify if you are working with ***integration*** deployment of Alert Logic MDR Services or ***production*** by specifying:

	```
	global_endpoint=integration
	```

	```
	global_endpoint=production
	```

	NOTE: If *global_endpoint* isn't present, SDK defaults to production.

3. Test installation
Launch python interpreter and then type:

	```
	>>> import almdrlib
	>>> aims = almdrlib.client("aims")
	>>> res = aims.get_account_details()
	>>> print(f"{res.json()}")
	```


## Development

### Getting Started
> Prerequisites:
>
1. Python v3.7 or older
2. virtualenv or virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>
>

Setup your development environment and install required dependencies:

```
$ export WORKON_HOME=~/environments
$ mkdir -p $WORKON_HOME
$ source /usr/local/bin/virtualenvwrapper.sh
$ mkvirtualenv alsdk
(alsdk) $ git clone https://github.com/alertlogic/alertlogic-sdk-python
(alsdk) $ cd alertlogic-sdk-python
(alsdk) $ pip install -r requirements.txt
(alsdk) $ pip install -e .
```
