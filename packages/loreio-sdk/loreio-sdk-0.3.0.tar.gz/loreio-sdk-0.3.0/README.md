Lore IO python SDK

Interactive shell:
    
    python -m loreiosdk wss://ui.getlore.io/storyteller

Scripting resources 
 
    from loreiosdk.spyglass_script import Spyglass
    spyglass_instance = Spyglass('wss://ui.getlore.io/storyteller', 'USERNAME',
    'PASSWORD', dataset_id='DATASET_ID')
  




Dev resources 

Build using:

    bumpversion --current-version VERSION minor setup.py loreiosdk/__init__.py
    
    python setup.py sdist bdist_wheel
Publish using: 

    twine upload dist/loreio-sdk-VERSION.tar.gz