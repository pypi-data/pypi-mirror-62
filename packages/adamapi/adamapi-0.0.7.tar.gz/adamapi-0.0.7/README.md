# Coding constraint ( EX Best practices )
1.  If python use 3 instead of 2.7
2.  If python indentation must be 4 spaces and NOT tab !important
3.  On log files never use the username but refer to the user by its [id]
4.  Remember that is git that maintain the versioning and do it quite well, for sure better than you. Remove unused code and don't invent home made and exotic code history and traceability based on comments
5.  Put a comment at the beginning of each function/method the summarize what's its scope
```python
def aMethod( self, var1, var2):
    """
    a comment here
    """"
```
6.  Mantain the documentation aligned with released software, in particular the api_definitions.md doc
7.  Mantain the test suite aligned with developed code
8.  Execute the test suite before deliver new software


# Installation

## Requirements

```bash
sudo apt-get install python3-venv python3-gdal gdal-bin
```

## Install from git
```bash
cd /opt
git clone https://git.services.meeo.it/das/adamapi.git
cd adamapi
VENVNAME="venv"
python3 -m venv "${VENVNAME}"
source "${VENVNAME}/bin/activate";
python3 -m pip install --upgrade pip
pip install -r requirements.txt
ln -s "/usr/lib/python3/dist-packages/osgeo" "/opt/adamapi/${VENVNAME}/lib/python3.7/site-packages/osgeo"
ln -s /opt/adamapi /opt/adamapi/${VENVNAME}/lib/python3.7/site-packages/adamapi
```

## Install with pip
```bash
VENVNAME="adamapi"
python3 -m venv "${VENVNAME}"
source "${VENVNAME}/bin/activate";
python3 -m pip install --upgrade pip;
pip install adamapi
ln -s "/usr/lib/python3/dist-packages/osgeo" "${VENVNAME}/lib/python3.7/site-packages/osgeo"
```
