```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
source setenv.sh
python es_create_index_and_mapping.py
python es_get_settings.py
python es_analize.py
python es_create_document.py
python es_search_document.py
python es_update_document.py
python es_delete.py
```
