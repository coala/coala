@echo ON

REM Install deps using pip
%CMD_IN_ENV% pip -q install coverage pylint setuptools munkres3

REM Install GNU gettext
nuget install Gettext.Tools -Version 0.19.4
SET PATH=%PATH%;%cd%\Gettext.Tools.0.19.4\tools

REM Install eSpeak printer
curl -LO http://sourceforge.net/projects/espeak/files/espeak/espeak-1.48/setup_espeak-1.48.04.exe
setup_espeak-1.48.04.exe /NORESTART /SUPPRESSMSGBOXES /VERYSILENT /SP-
SET PATH=%PATH%;C:\Program Files (x86)\eSpeak\command_line

@echo OFF
