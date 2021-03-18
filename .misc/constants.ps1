
New-Variable -Scope global -Name project_name -Value 'coala'
New-Variable -Scope global -Name pip_version -Value '9.0.3'
New-Variable -Scope global -Name setuptools_version -Value '21.2.2'

$old_EAP = $ErrorActionPreference
$ErrorActionPreference = 'SilentlyContinue'
Export-ModuleMember -Variable name, pip_version, setuptools_version
$ErrorActionPreference = $old_EAP
