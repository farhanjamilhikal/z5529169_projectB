@echo off
setlocal
set "MPLCONFIGDIR=%CD%\.runtime_cache\matplotlib"
set "NLTK_DATA=%CD%\.runtime_cache\nltk_data"
python scripts\run_all.py
endlocal
