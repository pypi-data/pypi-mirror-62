#Lore IO python SDK


Interactive shell:
```bash 
python -m loreio-sdk wss://ui.getlore.io/storyteller
 ```
Scripting resources 
 ```python
from loreiosdk.spyglass_script import Spyglass   

# get your spyglass instance
spyglass_instance = Spyglass('wss://ui.getlore.io/storyteller', 'USERNAME',
'PASSWORD', dataset_id='DATASET_ID')

# sync_cmd will trigger an syncronous command and will return (status, seqno, result)
spyglass_instance.sync_cmd("Command Name", ["Positional_argument"], {"Keyword_arg": True})
```

  

##Contributors resources 

Build using:
```bash
bumpversion --current-version VERSION minor setup.py loreiosdk/__init__.py

python setup.py sdist bdist_wheel  
```
Publish using: 
```bash
twine upload dist/loreio-sdk-VERSION.tar.gz
```