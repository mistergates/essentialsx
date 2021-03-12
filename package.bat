@ECHO OFF
CHOICE /M "Build for production"?
IF ERRORLEVEL 1 SET REPO=
IF ERRORLEVEL 2 SET REPO=--repository testpypi

@ECHO ON
%~dp0\venv\bin\python -m pip install --upgrade build
%~dp0\venv\bin\python -m pip install --upgrade twine

%~dp0\venv\bin\python -m build
%~dp0\venv\bin\python -m twine upload %REPO% dist/*