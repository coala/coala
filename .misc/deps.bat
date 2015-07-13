@echo ON

REM Install deps using pip
%CMD_IN_ENV% pip -q install coverage pylint setuptools munkres3

REM Install GNU gettext
nuget install Gettext.Tools -Version 0.19.4
SET PATH=%PATH%;%cd%\Gettext.Tools.0.19.4\tools

@echo OFF
