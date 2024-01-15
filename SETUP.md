# Development Set-up
## Prerequisites
* Python 3
* NumPy (package)
* twofish (package)
* PyQt5 (package)
## Instructions
1. If you don't have Python 3 version 3.9 and above installed, download and install from here [Python 3](https://www.python.org/downloads/).
   
3. From the source directory, run the following command to create a virtual environment and activate it (recommended)
#### Windows (Powershell/CMD):
```powershell
python -m venv venv
(Powershell) venv\Scripts\Activate
(CMD) venv\Scripts\activate
```
For `Activate.ps1 cannot be loaded because running scripts is disabled on this system` error in powershell, run this command:
 ```powershell
Set-ExecutionPolicy -Scope CurrentUser Unrestricted
```
and try activating the venv again.

#### Linux (bash):
```bash
python3 -m venv venv
source venv/bin/activate
```
> note: you might need install venv first before you can create a virtual environment
- you can skip this step and proceed immediately to Step 3 but using a virual environemt is highly recommended

3. Install the packages from `requirements.txt` :
```
pip install -r requirements.txt
```

4. You can now run `main.py` if you want to use the GUI or run the `embed.py` and `extract.py` scripts directly:
#### GUI:
```python
python main.py
```
#### direct scripts (-h for help on how to use):
```
python embed.py -h
python embed.py <audiofile> <message>
or
python embed.py <audiofile> <message> -p <password>
```
```
python extract.py -h
python extract.py <stegofile> <key>
or
python extract.py <stegofile> <key> -p <password>
```
> note: use `.wav` audio files


---------------------
SUS: https://forms.gle/v9KTRUuQLzRWufDo9