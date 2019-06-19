
function Write-Success
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Message,

        [switch]
        $NoNewLine
    )

    Write-Host $Message -NoNewline:$NoNewLine -ForegroundColor Green
}

function Write-Information
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Message,

        [switch]
        $NoNewLine
    )

    Write-Host $Message -NoNewline:$NoNewLine -ForegroundColor Magenta
}


function Write-Details
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Message,

        [switch]
        $NoNewLine
    )

    Write-Host $Message -NoNewline:$NoNewLine -ForegroundColor Cyan
}


function Write-Notice
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Message,

        [switch]
        $NoNewLine
    )

    Write-Host $Message -NoNewline:$NoNewLine -ForegroundColor Yellow
}


function Write-Fail
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Message,

        [switch]
        $NoNewLine
    )

    Write-Host $Message -NoNewline:$NoNewLine -ForegroundColor Red
}


# compares two versions, and returns a value specifying if they're equal or different
# -1: installed version is behind
#  0: installed version is latest
#  1: installed version is ahead
function Compare-Versions
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Installed,

        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $NewVersion
    )

    if (Test-VersionPassedIsLatest $NewVersion) {
        return -1
    }

    $i_parts = $Installed -split '\.'
    $o_parts = $NewVersion -split '\.'

    $count = $i_parts.Length
    if ($o_parts.Length -gt $count) {
        $count = $o_parts.Length
    }

    for ($i = 0; $i -lt $count; $i++)
    {
        if ($i_parts[$i] -eq $o_parts[$i]) {
            continue
        }

        if ($i_parts[$i] -lt $o_parts[$i]) {
            return -1
        }
        else {
            return 1
        }
    }

    return 0
}


# takes a package about to be installed, and checks if the version needs to be installed,
# or just a downgrade/upgrade of what's already installed
function Get-InstallAction
{
    param (
        [string]
        $Package,

        [string]
        $Version,

        $LocalList
    )

    # if it's not installed, it needs installing
    $current = $LocalList[$Package]
    if (Test-Empty $current) {
        return 'install'
    }

    # compare the version, and determine if we need to upgrade/downgrade
    $action = Compare-Versions -Installed $current -NewVersion $Version

    switch ($action)
    {
        1 { return 'downgrade' }
        -1 { return 'upgrade' }
        default { return 'install' }
    }
}


# return the package name from a supplied key
function Get-PackageFromKey
{
    param (
        [string]
        $Key
    )

    return ($Key -isplit '@')[0].Trim()
}


# return the version from a supplied key
function Get-VersionFromKey
{
    param (
        [string]
        $Key
    )

    $parts = ($Key -isplit '@')
    if ($parts.Length -le 1) {
        return 'latest'
    }

    return $parts[1].Trim()
}


# returns the levenshtein distance between two strings
function Get-Levenshtein
{
    param (
        [string]
        $Value1,

        [string]
        $Value2
    )

    $len1 = $Value1.Length
    $len2 = $Value2.Length

    if ($len1 -eq 0) { return $len2 }
    if ($len2 -eq 0) { return $len1 }

    $Value1 = $Value1.ToLowerInvariant()
    $Value2 = $Value2.ToLowerInvariant()

    $dist = New-Object -Type 'int[,]' -Arg ($len1 + 1), ($len2 + 1)

    0..$len1 | ForEach-Object { $dist[$_, 0] = $_ }
    0..$len2 | ForEach-Object { $dist[0, $_] = $_ }

    $cost = 0

    for ($i = 1; $i -le $len1; $i++)
    {
        for ($j = 1; $j -le $len2; $j++)
        {
            $cost = 1
            if ($Value2[$j - 1] -ceq $Value1[$i - 1])
            {
                $cost = 0
            }

            $tempmin = [System.Math]::Min(([int]$dist[($i - 1), $j] + 1), ([int]$dist[$i, ($j - 1)] + 1))
            $dist[$i, $j] = [System.Math]::Min($tempmin, ([int]$dist[($i - 1), ($j - 1)] + $cost))
        }
    }

    # the actual distance is stored in the bottom right cell
    return $dist[$len1, $len2];
}


# safeguards a string, by return empty or a default if empty
function Format-SafeguardString
{
    param (
        [string]
        $Value,

        [string]
        $Default = $null
    )

    if (!(Test-Empty $Value)) {
        return $Value
    }

    $Value = [string]::Empty
    if (!(Test-Empty $Default)) {
        $Value = $Default
    }

    return $Value
}


# checks to see if a passed version is to use the latest version
function Test-VersionPassedIsLatest
{
    param (
        [string]
        $Version
    )

    return ((Test-Empty $Version) -or ($Version.Trim() -ieq 'latest'))
}


# checks to see if a passed path is a valid nuspec (path, xml, and content)
function Test-Nuspec
{
    param (
        [string]
        $Path
    )

    if (!(Test-NuspecPath $Path))
    {
        Write-Fail "Path to nuspec file doesn't exist or is invalid: $($Path)"
        return $false
    }

    if (!(Test-XmlContent $Path))
    {
        Write-Fail "Nuspec file fails to parse as a valid XML document: $($Path)"
        return $false
    }

    $nuspecData = Get-XmlContent $Path

    if (!(Test-NuspecContent $nuspecData))
    {
        Write-Fail "Nuspec file is missing the package/metadata XML sections: $($Path)"
        return $false
    }

    return $true
}


# checks to see if a passed path is a valid nuspec file path
function Test-NuspecPath
{
    param (
        [string]
        $Path
    )

    # ensure a path was passed
    if ([string]::IsNullOrWhiteSpace($Path))
    {
        return $false
    }

    # ensure path is exists, or is not just a directory path
    if (!(Test-Path $Path) -or (Test-PathDirectory $Path))
    {
        return $false
    }

    return $true
}


# checks to see if the file at passed path is a valid XML file
function Test-XmlContent
{
    param (
        [string]
        $Path
    )

    # fail if the path doesn't exist
    if ([string]::IsNullOrWhiteSpace($Path) -or !(Test-Path $Path))
    {
        return $false
    }

    # ensure the content parses as xml
    try
    {
        [xml](Get-Content $Path) | Out-Null
        return $true
    }
    catch [exception]
    {
        return $false
    }
}


# checks to see if the passed XML content is a valid nuspec file
function Test-NuspecContent
{
    param (
        [xml]
        $Content
    )

    return ($Content -ne $null -and $Content.package -ne $null -and $Content.package.metadata -ne $null)
}


# returns the XML content of the file at the passed path
function Get-XmlContent
{
    param (
        [string]
        $Path
    )

    if (!(Test-XmlContent $Path))
    {
        return $null
    }

    return [xml](Get-Content $Path)
}


# checks to see if a passed path is a directory
function Test-PathDirectory
{
    param (
        [string]
        $Path
    )

    if ([string]::IsNullOrWhiteSpace($Path) -or !(Test-Path $Path))
    {
        return $false
    }

    return ((Get-Item $Path) -is [System.IO.DirectoryInfo])
}


# returns a path to a fidgefile based on a passed path
function Get-FudgefilePath
{
    param (
        [string]
        $Path,

        [switch]
        $Adhoc
    )

    if ($Adhoc)
    {
        return [string]::Empty
    }

    $rootpath = './Fudgefile'
    if (![string]::IsNullOrWhiteSpace($Path))
    {
        if ((Test-Path $Path) -and (Test-PathDirectory $Path))
        {
            $rootpath = Join-Path $Path 'Fudgefile'
        }
        else
        {
            $rootpath = $Path
        }
    }

    return $rootpath
}


# returns the content of a passed fudgefile path
function Get-FudgefileContent
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Path
    )

    if (!(Test-Path $Path)) {
        throw "Path to Fudgefile does not exist: $($Path)"
    }

    try {
        $config = Get-Content -Path $Path -Raw | ConvertFrom-Json
    }
    catch {
        throw "Failed to parse the Fudgefile at: $($Path)`n$($_.Exception)"
    }

    return $config
}


# removes an existing fudgefile, and if passed attempting to uninstall the packages
function Remove-Fudgefile
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Path,

        $LocalList,

        [switch]
        $Uninstall,

        [switch]
        $Dev,

        [switch]
        $DevOnly
    )

    # ensure the path actually exists
    if (!(Test-Path $Path))
    {
        Write-Fail "Path to Fudgefile does not exist: $($Path)"
        return
    }

    # uninstall packages first, if requested
    if ($Uninstall)
    {
        $config = Get-FudgefileContent $Path
        Invoke-ChocolateyAction -Action 'uninstall' -Key $null -Config $config -LocalList $LocalList -Dev:$Dev -DevOnly:$DevOnly
    }

    # remove the fudgefile
    Write-Information "> Deleting Fudgefile" -NoNewLine
    Remove-Item -Path $Path -Force -Confirm:$false | Out-Null
    Write-Success " > deleted"
    Write-Details "   > $($Path)"
}


# restores the packages of an existing fudgefile (either empty, from nuspec, or from local)
function Restore-Fudgefile
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Path,

        [string]
        $Key,

        $LocalList,

        [switch]
        $Install,

        [switch]
        $Uninstall,

        [switch]
        $Dev,

        [switch]
        $DevOnly
    )

    # retrieve the content of the current fudgefile
    $content = Get-FudgefileContent $Path

    # check to see if we're restoring this file using local packages
    if ($Key -ieq 'local')
    {
        if (Test-Empty $LocalList)
        {
            Write-Fail "No packages installed locally to renew Fudgefile"
            return
        }

        Write-Information "> Renewing Fudgefile using $($LocalList.Count) local packages" -NoNewLine
    }

    # check if there are any nuspecs in the pack section
    elseif ($Key -ieq 'nuspec')
    {
        if (Test-Empty $content.pack)
        {
            Write-Fail "No nuspecs in pack section to renew Fudgefile"
            return
        }

        Write-Information "> Renewing Fudgefile using nuspecs" -NoNewLine
    }

    # else if it's not empty, we don't know what they mean
    elseif (!(Test-Empty $Key))
    {
        Write-Fail "Renew command not recognised: $($Key). Should be blank, or either local/nuspec"
        return
    }

    # else we're renewing to an empty file
    else
    {
        Write-Information "> Renewing Fudgefile" -NoNewLine
    }

    # first, uninstall the packages, if requested
    if ($Uninstall)
    {
        Invoke-ChocolateyAction -Action 'uninstall' -Key $null -Config $content -LocalList $LocalList -Dev:$Dev -DevOnly:$DevOnly
    }

    # remove all current packages
    if (!$DevOnly)
    {
        $content.packages = @()
    }

    if ($Dev)
    {
        $content.devPackages = @()
    }

    # insert packages from any nuspecs in the pack section
    if ($Key -ieq 'nuspec')
    {
        $nuspecs = $content.pack.psobject.properties.name
        $nuspecs | ForEach-Object {
            $content = Add-PackagesFromNuspec -Content $content -Path $content.pack.$_ -Dev:$Dev -DevOnly:$DevOnly
        }
    }

    # insert any data from the local packages
    if ($Key -ieq 'local')
    {
        $content = Add-PackagesFromLocal -Content $content -LocalList $LocalList -DevOnly:$DevOnly
    }

    # save contents as json
    $content | ConvertTo-Json | Out-File -FilePath $Path -Encoding utf8 -Force
    Write-Success " > renewed"
    Write-Details "   > $($Path)"

    # now install the packages
    if ($Install)
    {
        Invoke-ChocolateyAction -Action 'install' -Key $null -Config $content -LocalList $LocalList -Dev:$Dev -DevOnly:$DevOnly
    }
}


# create a new empty fudgefile, or a new one from a nuspec file
function New-Fudgefile
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Path,

        [string]
        $Key,

        $LocalList,

        [switch]
        $Install,

        [switch]
        $Dev,

        [switch]
        $DevOnly
    )

    # check to see if we're making this file using local packages
    if ($Key -ieq 'local')
    {
        if (Test-Empty $LocalList)
        {
            Write-Fail "No packages installed locally to create new Fudgefile"
            return
        }

        Write-Information "> Creating new Fudgefile using $($LocalList.Count) local packages" -NoNewLine
    }

    # if the key is passed, ensure it's a valid nuspec file
    elseif (!(Test-Empty $Key))
    {
        if (!(Test-Nuspec $Key))
        {
            return
        }

        $nuspecName = Split-Path -Leaf -Path $Key
        Write-Information "> Creating new Fudgefile using $($nuspecName)" -NoNewLine
    }

    # else it's just an empty file
    else
    {
        Write-Information "> Creating new Fudgefile" -NoNewLine
    }

    # setup the empty fudgefile
    $content = @{
        'scripts' = @{
            'pre' = @{ 'install'= ''; 'uninstall'= ''; 'upgrade'= ''; 'downgrade' = ''; 'pack'= ''; };
            'post' = @{ 'install'= ''; 'uninstall'= ''; 'upgrade'= ''; 'downgrade' = ''; 'pack'= ''; };
        };
        'packages' = @();
        'devPackages' = @();
        'pack' = @{};
    }

    # insert any data from the nuspec
    if (!(Test-Empty $nuspecName))
    {
        $content = Add-PackagesFromNuspec -Content $content -Path $Key -Dev:$Dev -DevOnly:$DevOnly
        $name = [System.IO.Path]::GetFileNameWithoutExtension($nuspecName)
        $content.pack[$name] = $Key
    }

    # insert any data from the local packages
    if ($Key -ieq 'local')
    {
        $content = Add-PackagesFromLocal -Content $content -LocalList $LocalList -DevOnly:$DevOnly
    }

    # save contents as json
    $content | ConvertTo-Json | Out-File -FilePath $Path -Encoding utf8 -Force
    Write-Success " > created"
    Write-Details "   > $($Path)"

    # now install the packages
    if ($Install)
    {
        $config = Get-FudgefileContent $Path
        Invoke-ChocolateyAction -Action 'install' -Key $null -Config $config -LocalList $LocalList -Dev:$Dev -DevOnly:$DevOnly
    }
}


# adds packages to a fudgefile from local packages
function Add-PackagesFromLocal
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNull()]
        $Content,

        [Parameter(Mandatory=$true)]
        [ValidateNotNull()]
        $LocalList,

        [switch]
        $DevOnly
    )

    $LocalList.Keys | ForEach-Object {
        $package = @{
            'name' = $_;
            'version' = $LocalList[$_];
        }

        if ($DevOnly)
        {
            $Content.devPackages += $package
        }
        else
        {
            $Content.packages += $package
        }
    }

    return $Content
}


# adds packages to a fudgefile from a nuspec file
function Add-PackagesFromNuspec
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNull()]
        $Content,

        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        $Path,

        [switch]
        $Dev,

        [switch]
        $DevOnly
    )

    # get the content from the nuspec
    $data = Get-XmlContent -Path $Path
    $metadata = $data.package.metadata

    # if we have any dependencies, add them as packages
    if (!$DevOnly -and $metadata.dependencies -ne $null)
    {
        $metadata.dependencies.dependency | ForEach-Object {
            $version = Format-SafeguardString $_.version 'latest'
            $Content.packages += @{
                'name' = $_.id;
                'version' = $version;
            }
        }
    }

    # if we have any devDependencies, add them as devPackages
    if ($Dev -and $metadata.devDependencies -ne $null)
    {
        $metadata.devDependencies.dependency | ForEach-Object {
            $version = Format-SafeguardString $_.version 'latest'
            $Content.devPackages += @{
                'name' = $_.id;
                'version' = $version;
            }
        }
    }

    return $Content
}


# checks to see if the user has administrator privileges
function Test-AdminUser
{
    if ($PSVersionTable.Platform -ieq 'Unix')
    {
        Write-Notice 'Windows Admin check bypassed on Unix'
        return $true
    }

    try
    {
        $principal = New-Object System.Security.Principal.WindowsPrincipal([System.Security.Principal.WindowsIdentity]::GetCurrent())

        if ($principal -eq $null)
        {
            return $false
        }

        return $principal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)
    }
    catch [exception]
    {
        Write-Fail 'Error checking user administrator privileges'
        Write-Fail $_.Exception.Message
        return $false
    }
}


# checks to see if the passed value is empty
function Test-Empty
{
    param (
        $Value
    )

    if ($Value -eq $null)
    {
        return $true
    }

    if ($Value.GetType().Name -ieq 'string')
    {
        return [string]::IsNullOrWhiteSpace($Value)
    }

    $type = $Value.GetType().BaseType.Name.ToLowerInvariant()
    switch ($type)
    {
        'valuetype'
            {
                return $false
            }

        'array'
            {
                return (($Value | Measure-Object).Count -eq 0 -or $Value.Count -eq 0)
            }
    }

    return ([string]::IsNullOrWhiteSpace($Value) -or ($Value | Measure-Object).Count -eq 0 -or $Value.Count -eq 0)
}


# check to see if chocolatey is installed on the current machine
function Test-Chocolatey
{
    try {
        $output = Invoke-Expression -Command 'choco -v'
        Write-Details "Chocolatey v$($output)"
        return $true
    }
    catch {
        return $false
    }
}


# installs chocolatey
function Install-Chocolatey
{
    Write-Notice "Installing Chocolatey"

    $policies = @('Unrestricted', 'ByPass', 'AllSigned')
    if ($policies -inotcontains (Get-ExecutionPolicy)) {
        Set-ExecutionPolicy Bypass -Force
    }

    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')) | Out-Null
    Write-Success "Chocolatey installed`n"
}


# invoke scripts for pre/post actions
function Invoke-Script
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Action,

        [string]
        $Stage,

        $Scripts
    )

    # if there is no stage, return
    if (Test-Empty $Stage) {
        return
    }

    # if there are no scripts, return
    if ((Test-Empty $Scripts) -or (Test-Empty $Scripts.$Stage)) {
        return
    }

    $script = $Scripts.$Stage.$Action
    if (Test-Empty $script) {
        return
    }

    # run the script
    Invoke-Expression -Command $script
}


# cycle through the passed packages, actioning upon them
function Start-ActionPackages
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Action,

        [string]
        $Key,

        [string]
        $Source,

        [array]
        $Packages,

        [string]
        $Arguments,

        $LocalList
    )

    # if there are no packages to deal with, return
    if (Test-Empty $Packages) {
        return
    }

    # have we installed anything
    $installed = $false
    $haveKey = (![string]::IsNullOrWhiteSpace($Key))

    # loop through each of the packages, and call chocolatey on them
    foreach ($pkg in $Packages)
    {
        # skip if we forcing action on a specific package
        if ($haveKey -and ($pkg.name -ine $Key)) {
            continue
        }

        # use a package specific custom source
        if (![string]::IsNullOrWhiteSpace($pkg.source)) {
            $Source = $pkg.source
        }

        # force a specific action on the package
        $_action = $Action
        if (!(Test-Empty $pkg.action)) {
            $_action = $pkg.action
        }

        $installed = $true

        Invoke-Chocolatey -Action $_action -Package $pkg.name -Version $pkg.version `
            -Source $Source -Parameters $pkg.params -Arguments "$($pkg.args) $($Arguments)".Trim() -LocalList $LocalList
    }

    # if we didn't install anything, and we have a key - say it isn't present in file
    if (!$installed -and $haveKey) {
        Write-Notice "Package not found in Fudgefile: $($Key)"
    }
}


# cycle through the passed nuspecs for packing via nuget
function Start-ActionPack
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Action,

        [string]
        $Key,

        $Nuspecs
    )

    # if there are no nuspecs to deal with, return
    if (Test-Empty $Nuspecs) {
        return
    }

    # have we packed anything
    $packed = $false
    $haveKey = (![string]::IsNullOrWhiteSpace($Key))

    # loop through each of the nuspecs, and call chocolatey on them for packing
    foreach ($pkg in $Nuspecs.psobject.properties.name)
    {
        if ($haveKey -and ($pkg -ine $Key)) {
            continue
        }

        $packed = $true
        Invoke-Chocolatey -Action $Action -Package $pkg -Version ($Nuspecs.$pkg)
    }

    # if we didn't pavk anything, and we have a key - say it isn't present in file
    if (!$packed -and $haveKey) {
        Write-Notice "Nuspec not found in Fudgefile: $($Key)"
    }
}


# invokes a chocolatey action, which also runs the pre/post scripts
function Invoke-ChocolateyAction
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Action,

        [string]
        $Key,

        [string]
        $Source,

        $Config,

        $LocalList,

        [string]
        $Parameters,

        [string]
        $Arguments,

        [switch]
        $Dev,

        [switch]
        $DevOnly,

        [switch]
        $Adhoc
    )

    # ensure the config object exists, unless adhoc is supplied
    if (!$Adhoc -and $null -eq $Config) {
        throw "Invalid Fudge configuration supplied"
    }

    # if we're running as adhoc, just call chocolatey directly
    if ($Adhoc)
    {
        $pkg = Get-PackageFromKey -Key $Key
        $vsn = Get-VersionFromKey -Key $Key
        Invoke-Chocolatey -Action $Action -Package $pkg -Source $Source -Version $vsn -LocalList $LocalList -Parameters $Parameters -Arguments $Arguments
    }
    else
    {
        # invoke pre-script for current action
        Invoke-Script -Action $Action -Stage 'pre' -Scripts $Config.scripts

        # invoke chocolatey based on the action
        switch ($Action.ToLowerInvariant()) {
            'pack' {
                # run pack on supplied nuspecs
                Start-ActionPack -Action $Action -Key $Key -Nuspecs $Config.pack
            }

            default {
                # install normal packages, unless flagged as dev only
                if (!$DevOnly) {
                    Start-ActionPackages -Action $Action -Key $Key -Packages $Config.packages -Source $Source -LocalList $LocalList -Arguments $Arguments
                }

                # install dev packages
                if ($Dev) {
                    Start-ActionPackages -Action $Action -Key $Key -Packages $Config.devPackages -Source $Source -LocalList $LocalList -Arguments $Arguments
                }
            }
        }

        # invoke post-script for current action
        Invoke-Script -Action $Action -Stage 'post' -Scripts $Config.scripts
    }
}


# add the core chocolatey and fudge packages to a package map
function Add-CoreChocoPackages
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNull()]
        $Packages
    )

    $Packages['chocolatey'] = 'latest'
    $Packages['chocolatey-core.extension'] = 'latest'
    $Packages['fudge'] = 'latest'

    return $Packages
}


# pruning the current machine's packages with what's in the fudgefile
function Invoke-FudgePrune
{
    param (
        $Config,

        $LocalList,

        [switch]
        $Dev,

        [switch]
        $DevOnly
    )

    # package map for what to leave installed
    $packages = @{}
    $pruned = $false

    if (!$DevOnly)
    {
        $Config.packages | ForEach-Object { $packages[$_.name] = $_.version }
    }

    if ($Dev)
    {
        $Config.devPackages | ForEach-Object { $packages[$_.name] = $_.version }
    }

    # add core chocolatey packages (and fudge)
    $packages = Add-CoreChocoPackages $packages

    # loop through each local package, and remove if not in fudgefile
    $LocalList.Keys | ForEach-Object {
        if (!$packages.ContainsKey($_))
        {
            $pruned = $true
            Invoke-Chocolatey -Action 'uninstall' -Package $_
        }
    }

    if(!$pruned)
    {
        Write-Notice 'Nothing to prune'
    }
}


# cleaning a machine of all packages currently installed
function Invoke-FudgeClean
{
    param (
        $LocalList
    )

    # package map for what to leave installed
    $packages = @{}
    $cleaned = $false

    # add core chocolatey packages (and fudge)
    $packages = Add-CoreChocoPackages $packages

    # loop through each local package, and remove it
    $LocalList.Keys | ForEach-Object {
        if (!$packages.ContainsKey($_))
        {
            $cleaned = $true
            Invoke-Chocolatey -Action 'uninstall' -Package $_
        }
    }

    if(!$cleaned)
    {
        Write-Notice 'Nothing to clean'
    }
}


# add a package to a fudgefile
function Invoke-FudgeAdd
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Path,

        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Key,

        [string]
        $Source,

        $Config,

        $LocalList,

        [string]
        $Parameters,

        [string]
        $Arguments,

        [switch]
        $Dev,

        [switch]
        $Install
    )

    # get name and version from key
    $KeyName = Get-PackageFromKey -Key $Key
    $KeyVer = Get-VersionFromKey -Key $Key

    # ensure package isn't already present
    $pkg_count = ($config.packages | Where-Object { $_.name -ieq $KeyName } | Measure-Object).Count
    $dev_count = ($config.devPackages | Where-Object { $_.name -ieq $KeyName } | Measure-Object).Count

    if ($pkg_count -ne 0 -or $dev_count -ne 0)
    {
        Write-Notice "The package '$($KeyName)' already exists in the Fudgefile"
        return
    }

    # attempt to install if specified
    if ($Install)
    {
        Invoke-Chocolatey -Action 'install' -Package $KeyName -Source $Source -Version $KeyVer -LocalList $LocalList -Parameters $Parameters -Arguments $Arguments
    }

    Write-Information "> Adding $($KeyName)@$($KeyVer) to Fudgefile" -NoNewLine

    # create package json object
    $obj = @{ 'name' = $KeyName; }

    if (!(Test-Empty $KeyVer))
    {
        $obj['version'] = $KeyVer
    }

    if (!(Test-Empty $Source) -and ($Source -ine $Config.source))
    {
        $obj['source'] = $Source
    }

    # add to config
    if ($Dev)
    {
        [array]$Config.devPackages += $obj
    }
    else
    {
        [array]$Config.packages += $obj
    }

    # save new config back
    $Config | ConvertTo-Json | Out-File -FilePath $Path -Encoding utf8 -Force
    Write-Success " > added"
    Write-Details "   > $($Path)"
}


# removes a package from a fudgefile
function Invoke-FudgeRemove
{
    param (
        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Path,

        [Parameter(Mandatory=$true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $Key,

        $Config,

        $LocalList,

        [string]
        $Parameters,

        [string]
        $Arguments,

        [switch]
        $Dev,

        [switch]
        $Uninstall
    )

    # get name and version from key
    $KeyName = Get-PackageFromKey -Key $Key

    # ensure package isn't already removed
    $pkg_count = ($config.packages | Where-Object { $_.name -ieq $KeyName } | Measure-Object).Count
    $dev_count = ($config.devPackages | Where-Object { $_.name -ieq $KeyName } | Measure-Object).Count

    if ($pkg_count -eq 0 -and $dev_count -eq 0)
    {
        Write-Notice "The package '$($KeyName)' is not present in the Fudgefile"
        return
    }

    # attempt to uninstall if specified
    if ($Uninstall)
    {
        Invoke-Chocolatey -Action 'uninstall' -Package $KeyName -LocalList $LocalList -Parameters $Parameters -Arguments $Arguments
    }

    Write-Information "> Removing $($KeyName) from Fudgefile" -NoNewLine

    # remove to config
    if ($Dev)
    {
        $Config.devPackages = ($Config.devPackages | Where-Object { $_.name -ine $KeyName })
    }
    else
    {
        $Config.packages = ($Config.packages | Where-Object { $_.name -ine $KeyName })
    }

    # save new config back
    $Config | ConvertTo-Json | Out-File -FilePath $Path -Encoding utf8 -Force
    Write-Success " > removed"
    Write-Details "   > $($Path)"
}


# returns the path for where a command is located
function Invoke-FudgeWhich
{
    param (
        [string]
        $Key
    )

    if (Test-Empty $Key)
    {
        Write-Notice 'No command passed to find'
    }
    else
    {
        $path = (Get-Command -Name $Key -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Definition)
        if (!(Test-Empty $path))
        {
            Write-Host "> $($path)"
        }
        else
        {
            Write-Notice "Command not found: $($Key)"
        }
    }
}


# returns a source argument for chocolatey
function Format-ChocolateySource
{
    param (
        [string]
        $Source
    )

    if (Test-Empty $Source) {
        return [string]::Empty
    }

    return "-s '$($Source)'"
}


# returns a params argument for chocolatey
function Format-ChocolateyParams
{
    param (
        [string]
        $Parameters
    )

    if (Test-Empty $Parameters) {
        return [string]::Empty
    }

    return "--params='$($Parameters)'"
}


# returns a version argument for chocolatey
function Format-ChocolateyVersion
{
    param (
        [string]
        $Version
    )

    # if the version is latest, return empty
    if (Test-VersionPassedIsLatest -Version $Version) {
        return [string]::Empty
    }

    # return the specific version to install
    return "--version $($Version)"
}


# returns the list of search returns from chocolatey
function Get-ChocolateySearchList
{
    param (
        [string]
        $Key,

        [string]
        $Source
    )

    # set the source if we have one
    $Source = Format-ChocolateySource $Source

    $list = (choco search $Key $Source)
    if (!$?) {
        Write-Fail "$($list)"
        throw 'Failed to retrieve search results from Chocolatey'
    }

    return (Format-ChocolateyList -List $list)
}


# returns a list of packages installed localled
function Get-ChocolateyLocalList
{
    $list = (choco list -lo)
    if (!$?) {
        Write-Fail "$($list)"
        throw 'Failed to retrieve local list of installed packages'
    }

    return (Format-ChocolateyList -List $list)
}


# formats list/search results from chocolatey into a hash table
function Format-ChocolateyList
{
    param (
        [string[]]
        $List
    )

    $map = @{}

    $List | ForEach-Object {
        $row = $_ -ireplace ' Downloads cached for licensed users', ''
        if ($row -imatch '^(?<name>.*?)\s+(?<version>[\d\.]+(\s+\[Approved\]){0,1}(\s+-\s+Possibly broken){0,1}).*?$')
        {
            $map[$Matches['name']] = $Matches['version']
        }
    }

    return $map
}

# get chocolatey search results, filtered by fudge
function Format-ChocolateySearchResults
{
    param (
        [Parameter()]
        [string]
        $Key,

        [Parameter()]
        [int]
        $Limit,

        [Parameter()]
        [string]
        $Source
    )

    # get search results from chocolatey
    $results = Get-ChocolateySearchList -Key $Key -Source $Source
    $OrganisedResults = @()
    $count = 0

    # if limit is 0, set to total results returned
    if ($Limit -eq 0) {
        $Limit = ($results | Measure-Object).Count
    }

    # perfect match result
    if ($results.ContainsKey($Key)) {
        $count++
        $OrganisedResults += @{ 'Name' = $Key; 'Version' = $results[$Key]; }
        $results.Remove($Key)
    }

    # starts with for sub-packages
    if ($count -lt $Limit)
    {
        $results.Clone().Keys | ForEach-Object {
            if ($_.StartsWith("$($Key).")) {
                $count++
                $OrganisedResults += @{ 'Name' = $_; 'Version' = $results[$_]; }
                $results.Remove($_)
            }
        }
    }

    # starts with for other packages
    if ($count -lt $Limit)
    {
        $results.Clone().Keys | ForEach-Object {
            if ($_.StartsWith($Key)) {
                $count++
                $OrganisedResults += @{ 'Name' = $_; 'Version' = $results[$_]; }
                $results.Remove($_)
            }
        }
    }

    # contains the key
    if ($count -lt $Limit)
    {
        $results.Clone().Keys | ForEach-Object {
            if ($_.Contains($Key)) {
                $count++
                $OrganisedResults += @{ 'Name' = $_; 'Version' = $results[$_]; }
                $results.Remove($_)
            }
        }
    }

    # levenshtein for remaining packages
    if ($count -lt $Limit)
    {
        $leven = @()

        $results.Keys | ForEach-Object {
            $leven += @{ 'Name' = $_; 'Version' = $results[$_]; 'Dist' = (Get-Levenshtein $Key $_) }
        }

        $leven | Sort-Object { $_.Dist } | ForEach-Object {
            $OrganisedResults += @{ 'Name' = $_.name; 'Version' = $_.Version; }
        }
    }

    return @($OrganisedResults)
}


# invokes fudge to search chocolatey for a package and display the results
function Invoke-Search
{
    param (
        [string]
        $Key,

        [int]
        $Limit,

        [string]
        $Source,

        $LocalList
    )

    # validate the key/package name supplied
    if ([string]::IsNullOrWhiteSpace($Key)) {
        Write-Notice 'No search key provided'
        return
    }

    # validate the limit supplied
    if ($Limit -lt 0) {
        Write-Notice "Limit for searching must be 0 or greater, found: $($Limit)"
        return
    }

    # get search results from chocolatey
    $results = Format-ChocolateySearchResults -Key $Key -Limit $Limit -Source $Source

    # display the search results
    $results | Select-Object -First $Limit | ForEach-Object {
        if ($LocalList.ContainsKey($_.Name))
        {
            ($_.Version -imatch '^(?<version>[\d\.]+).*?$') | Out-Null

            if ($Matches['version'] -eq $LocalList[$_.Name]) {
                Write-Success ("{0,-30} {1,-40} (installed: {2})" -f $_.Name, $_.Version, $LocalList[$_.Name])
            }
            else {
                Write-Notice ("{0,-30} {1,-40} (installed: {2})" -f $_.Name, $_.Version, $LocalList[$_.Name])
            }
        }
        else {
            Write-Host ("{0,-30} {1,-30}" -f $_.Name, $_.Version)
        }
    }

    # display the total
    $total = ($results | Measure-Object).Count
    Write-Notice "$($total) package(s) found"
}


# invokes fudge to display details of local packages
function Invoke-FudgeLocalDetails
{
    param (
        $Config,

        [string]
        $Key,

        $LocalList,

        [switch]
        $Dev,

        [switch]
        $DevOnly
    )

    # maps for filtering packages
    $installed = @{}
    $updating = @{}
    $missing = @{}

    # package map
    $packages = @{}

    if (!$DevOnly) {
        $Config.packages | ForEach-Object { $packages[$_.name] = $_.version }
    }

    if ($Dev) {
        $Config.devPackages | ForEach-Object { $packages[$_.name] = $_.version }
    }

    # loop through packages
    $packages.Keys | ForEach-Object {
        if ([string]::IsNullOrWhiteSpace($Key) -or $_ -ieq $Key)
        {
            $version = $packages[$_]

            if ($LocalList.ContainsKey($_))
            {
                if ($LocalList[$_] -ieq $version -or (Test-VersionPassedIsLatest $version)) {
                    $installed[$_] = $version
                }
                else {
                    $updating[$_] = $version
                }
            }
            else {
                $missing[$_] = $version
            }
        }
    }

    if (![string]::IsNullOrWhiteSpace($Key) -and (Test-Empty $installed) -and (Test-Empty $updating) -and (Test-Empty $missing))
    {
        $missing[$Key] = 'Not in Fudgefile'
    }

    # output the details
    Write-Host "Package details from Fudgefile:"
    $installed.Keys | Sort-Object | ForEach-Object { Write-Success ("{0,-30} {1,-20} (installed: {2})" -f $_, $installed[$_], $LocalList[$_]) }
    $updating.Keys | Sort-Object | ForEach-Object { Write-Notice ("{0,-30} {1,-20} (installed: {2})" -f $_, $updating[$_], $LocalList[$_]) }
    $missing.Keys | Sort-Object | ForEach-Object { Write-Fail ("{0,-30} {1,-20}" -f $_, $missing[$_]) }
}

function Get-ChocolateyLatestVersion
{
    param (
        [Parameter()]
        [string]
        $Package,

        [Parameter()]
        [string]
        $Source
    )

    $result = (Format-ChocolateySearchResults -Key $Package -Limit 1 -Source $Source | Select-Object -First 1)
    if (!(Test-Empty $result)) {
        return ($result.Version -split '\s+')[0]
    }

    return 'latest'
}

# invoke chocolate for the specific action
function Invoke-Chocolatey
{
    param (
        [Parameter()]
        [string]
        $Action,

        [Parameter()]
        [string]
        $Package,

        [Parameter()]
        [string]
        $Version,

        [Parameter()]
        [string]
        $Source,

        [Parameter()]
        [string]
        $Parameters,

        [Parameter()]
        [string]
        $Arguments,

        [Parameter()]
        $LocalList
    )

    # if there was no package passed, return
    if (Test-Empty $Package) {
        return
    }

    # set the source from which to install/upgrade/downgrade packages
    $SourceArg = Format-ChocolateySource $Source

    # set the parameters to pass
    $ParametersArg = Format-ChocolateyParams $Parameters

    $Arguments += ' --allow-unofficial'

    # if the version is latest, attempt to get the real current version
    $latest = Test-VersionPassedIsLatest -Version $Version
    if ($latest) {
        $Version = Get-ChocolateyLatestVersion -Package $Package -Source $Source
    }

    $Version = Format-SafeguardString $Version 'latest'

    # build a version string, so if latest we can show the latest version
    $VersionStr = "$($Version)"
    if ($latest) {
        $VersionStr = "latest [$($Version)]"
    }

    # set the version arg to pass
    $VersionArg = Format-ChocolateyVersion $Version

    # if action is 'install', do we need to install, or upgrade/downgrade based on version?
    if (($Action -ieq 'install') -and ($null -ne $LocalList)) {
        $Action = Get-InstallAction -Package $Package -Version $Version -LocalList $LocalList
    }

    # attempt 3 times - mostly do to help prevent timeouts
    foreach ($i in 1..3)
    {
        $success = $true

        # run chocolatey for appropriate action
        switch ($Action.ToLowerInvariant())
        {
            'install'
                {
                    if ($i -eq 1) {
                        Write-Information "> Installing $($Package) ($($VersionStr))" -NoNewLine
                    }
                    $output = Invoke-Expression "choco install $($Package) $($VersionArg) -y $($SourceArg) $($ParametersArg) $($Arguments)"
                }

            'upgrade'
                {
                    if ($i -eq 1) {
                        Write-Information "> Upgrading $($Package) to ($($VersionStr))" -NoNewLine
                    }
                    $output = Invoke-Expression "choco upgrade $($Package) $($VersionArg) -y $($SourceArg) $($ParametersArg) $($Arguments)"
                }

            'downgrade'
                {
                    if ($i -eq 1) {
                        Write-Information "> Downgrading $($Package) to ($($VersionStr))" -NoNewLine
                    }
                    $output = Invoke-Expression "choco upgrade $($Package) $($VersionArg) -y $($SourceArg) $($ParametersArg) $($Arguments) --allow-downgrade"
                }

            'uninstall'
                {
                    if ($i -eq 1) {
                        Write-Information "> Uninstalling $($Package)" -NoNewLine
                    }
                    $output = Invoke-Expression "choco uninstall $($Package) -y -x $($ParametersArg) $($Arguments)"
                }

            'pack'
                {
                    Write-Information "> Packing $($Package)" -NoNewLine
                    $path = Split-Path -Parent -Path $Version
                    $name = Split-Path -Leaf -Path $Version

                    try {
                        Push-Location $path
                        $output = Invoke-Expression "choco pack $($name) $($Arguments)"
                    }
                    finally {
                        Pop-Location
                    }
                }
        }

        # determine if we failed, or if the exit code indicates a reboot is needed,
        # or we've timed out and need to try
        $lastcode = $LASTEXITCODE
        if (!$? -or (@(0, 3010) -notcontains $lastcode))
        {
            # flag as failure
            $success = $false

            # check if the package timed-out, so we can retry again
            if ($output -ilike '*the operation has timed out*') {
                Start-Sleep -Seconds 5
                continue
            }

            # double check that the error isn't a false positive
            switch ($Action)
            {
                {($_ -ieq 'uninstall')}
                    {
                        $success = ($output -ilike '*has been successfully uninstalled*' -or $output -ilike '*Cannot uninstall a non-existent package*')
                    }

                {($_ -ieq 'install') -or ($_ -ieq 'upgrade') -or ($_ -ieq 'downgrade')}
                    {
                        $success = ($output -ilike '*has been successfully installed*' -or $output -ilike '*has been installed*')
                    }
            }
        }

        # if we get here, break out
        break
    }

    # if not successful, output the error details
    if (!$success) {
        Write-Fail " > failed"
        Write-Notice "`n`n$($output)`n"
        throw "Failed to $($Action) package: $($Package)"
    }

    $actionVerb = ("$($Action)ed" -ireplace 'eed$', 'ed')

    if ($output -ilike '*exit code 3010*' -or $lastcode -eq 3010)
    {
        Write-Success " > $($actionVerb)" -NoNewLine
        Write-Notice " > Reboot Required"
    }
    else {
        Write-Success " > $($actionVerb)"
    }
}