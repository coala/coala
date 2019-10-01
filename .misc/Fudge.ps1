<#
    .SYNOPSIS
        Fudge is a tool to help you manage and version control Chocolatey packages required for environments to function

    .DESCRIPTION
        Fudge is a tool to help you manage and version control Chocolatey packages required for environments to function.
        This is done via a Fudgefile which allows you to specify packages (and their versions) to install. You can also
        specify dev-specific packages (like git, or fiddler)

        You are also able to define pre/post install/upgrade/downgrade/uninstall scripts for additional required functionality

        Furthermore, Fudge has a section to allow you to specify multiple nuspec files and pack the one you need

    .PARAMETER Action
        The action that Fudge should undertake
        Actions: install, upgrade, downgrade, uninstall, reinstall, pack, list, search, new, delete, prune, clean, rebuild,
                 which, help, renew, add, remove
        [Alias: -a]

    .PARAMETER Key
        The key represents a package/nuspec name in the Fudgefile
        [Actions: install, upgrade, downgrade, uninstall, reinstall, pack, new, which, renew, add, remove]
        [Alias: -k]

    .PARAMETER FudgefilePath
        This will override looking for a default 'Fudgefile' at the root of the current path, and allow you to specify
        other files instead. This allows you to have multiple Fudgefiles
        [Actions: install, upgrade, downgrade, uninstall, reinstall, pack, list, new, delete, prune, rebuild, renew, add, remove]
        [Default: ./Fudgefile]
        [Alias: -fp]

    .PARAMETER Limit
        This argument only applies for the 'search' action. It will limit the amount of packages returned when searching
        If 0 is supplied, the full list is returned
        [Actions: search]
        [Default: 10]
        [Alias: -l]

    .PARAMETER Source
        Passing this argument will allow you to specify custom source locations to get/download packages for Chocolatey.
        This allows you to install packages from local directories, or from custom Chocolatey servers. Passing this will
        also override the source specified in any Fudgefiles
        [Default: Chocolatey's server]
        [Actions: install, upgrade, downgrade, reinstall, search, rebuild, add]
        [Alias: -s]

    .PARAMETER Parameters
        This argument allows you to pass parameters to a chocolatey package, as if you were using "--params" on choco.
        For install/upgrade/downgrade/uninstall/reinstall, this argument only works when "-Adhoc" is also supplied
        [Default: Empty]
        [Actions: install, upgrade, downgrade, uninstall, reinstall, add]
        [Alias: -p]

    .PARAMETER Arguments
        This argument allows you to pass extra arguments to a chocolatey, such as "--x86" or "--ignore-checksum"
        For install/upgrade/downgrade/uninstall/reinstall, this argument only works when "-Adhoc" is also supplied
        [Default: Empty]
        [Actions: install, upgrade, downgrade, uninstall, reinstall, add]
        [Alias: -args]

    .PARAMETER Dev
        Switch parameter, if supplied will also action upon the devPackages in the Fudgefile
        [Actions: install, upgrade, downgrade, uninstall, reinstall, list, delete, prune, rebuild, add, remove]
        [Alias: -d]

    .PARAMETER DevOnly
        Switch parameter, if supplied will only action upon the devPackages in the Fudgefile
        [Actions: install, upgrade, downgrade, uninstall, reinstall, list, delete, prune, rebuild]
        [Alias: -do]

    .PARAMETER Install
        Switch parameter, if supplied will install packages after creating a new Fudgefile
        [Actions: new, renew, add]
        [Alias: -i]

    .PARAMETER Uninstall
        Switch parameter, if supplied will uninstall packages before deleting a Fudgefile
        [Actions: delete, renew, remove]
        [Alias: -u]

    .PARAMETER Adhoc
        Switch parameter, if supplied will install software from Chocolatey whether or not
        the package is in the Fudgefile
        [Actions: install, upgrade, downgrade, uninstall, reinstall]
        [Alias: -ad]

    .PARAMETER Version
        Switch parameter, if supplied will just display the current version of Fudge installed
        [Alias: -v]

    .PARAMETER Help
        Switch parameter, if supplied will just display help output
        [Alias: -h]

    .EXAMPLE
        fudge install

    .EXAMPLE
        fudge install -d    # to also install devPackages (-do will only install devPackages)

    .EXAMPLE
        fudge install git -ad   # installs git dispite not being in the Fudgefile

    .EXAMPLE
        fudge pack website

    .EXAMPLE
        fudge list

    .EXAMPLE
        fudge search checksum
#>
param (
    [Alias('a')]
    [string]
    $Action,

    [Alias('k')]
    [string]
    $Key,

    [Alias('fp')]
    [string]
    $FudgefilePath,

    [Alias('l')]
    [int]
    $Limit = 10,

    [Alias('s')]
    [string]
    $Source,

    [Alias('p')]
    [string]
    $Parameters,

    [Alias('args')]
    [string]
    $Arguments,

    [Alias('d')]
    [switch]
    $Dev,

    [Alias('do')]
    [switch]
    $DevOnly,

    [Alias('i')]
    [switch]
    $Install,

    [Alias('u')]
    [switch]
    $Uninstall,

    [Alias('v')]
    [switch]
    $Version,

    [Alias('h')]
    [switch]
    $Help,

    [Alias('ad')]
    [switch]
    $Adhoc
)

# ensure if there's an error, we stop
$ErrorActionPreference = 'Stop'


# Import required modules
$root = Split-Path -Parent -Path $MyInvocation.MyCommand.Path
Import-Module "$($root)\Modules\FudgeTools.psm1" -Force -ErrorAction Stop


# output the version
$ver = 'v$version$'
Write-Success "Fudge $($ver)"

# if we were only after the version, just return
if ($Version -or (@('v', 'version') -icontains $Action))
{
    return
}


# if action is just to display Help, show it and return
if ($Help -or (@('h', 'help') -icontains $Action))
{
    Write-Host "`nUsage: fudge <action>"
    Write-Host "`nWhere <action> is one of:"
    Write-Host "    add, clean, delete, downgrade, help, install, list, new, pack,"
    Write-Host "    prune, rebuild, reinstall, remove, renew, search, uninstall,"
    Write-Host "    upgrade, version, which"
    Write-Host ""
    return
}


try
{
    # start timer
    $timer = [DateTime]::UtcNow


    # ensure we have a valid action
    $packageActions = @('install', 'upgrade', 'uninstall', 'reinstall', 'list', 'rebuild', 'downgrade', 'add', 'remove')
    $maintainActions = @('prune')
    $packingActions = @('pack')
    $miscActions = @('search', 'clean', 'which')
    $newActions = @('new')
    $alterActions = @('delete', 'renew')

    $actions = ($packageActions + $maintainActions + $packingActions + $miscActions + $newActions + $alterActions)
    if ((Test-Empty $Action) -or $actions -inotcontains $Action) {
        Write-Fail "Unrecognised action supplied '$($Action)', should be either: $($actions -join ', ')"
        return
    }


    # actions that require chocolatey
    $isChocoAction = (@('which', 'add', 'remove', 'delete') -inotcontains $Action)
    if (!$isChocoAction -and ($Install -or $Uninstall)) {
        $isChocoAction = $true
    }


    # if adhoc was supplied for an invalid action
    if ($Adhoc -and @('install', 'uninstall', 'upgrade', 'downgrade', 'reinstall') -inotcontains $Action) {
        Write-Fail "Adhoc supplied for invalid action: $($Action)"
        return
    }

    # if adhoc supplied with no package name, fail
    if ($Adhoc -and [string]::IsNullOrWhiteSpace($Key)) {
        Write-Fail "No package name supplied for adhoc $($Action)"
        return
    }


    # if -devOnly is passed, set -dev to true
    if ($DevOnly) {
        $Dev = $true
    }


    # get the Fudgefile path, if adhoc is supplied set to empty
    $FudgefilePath = Get-FudgefilePath $FudgefilePath -Adhoc:$Adhoc


    # ensure that the Fudgefile exists (for certain actions), and deserialise it
    if (($packageActions + $maintainActions + $packingActions + $alterActions) -icontains $Action)
    {
        $config = $null

        # if adhoc is supplied, we don't need to get the content
        if (!$Adhoc) {
            if (!(Test-Path $FudgefilePath)) {
                Write-Fail "Path to Fudgefile does not exist: $($FudgefilePath)"
                return
            }

            $config = Get-FudgefileContent $FudgefilePath
        }

        # if we have a custom source in the config and no CLI source, set the source
        if ((Test-Empty $Source) -and ($null -ne $config) -and !(Test-Empty $config.source)) {
            $Source = $config.source
        }
    }

    # ensure that the Fudgefile doesn't exist
    elseif ($newActions -icontains $Action)
    {
        if (Test-Path $FudgefilePath) {
            Write-Fail "Path to Fudgefile already exists: $($FudgefilePath)"
            return
        }
    }


    # if there are no packages to install or nuspecs to pack, just return
    if ($null -ne $config)
    {
        # check nuspecs
        if ($packingActions -icontains $Action)
        {
            if (Test-Empty $config.pack) {
                Write-Notice "There are no nuspecs to $($Action)"
                return
            }

            if (![string]::IsNullOrWhiteSpace($Key) -and [string]::IsNullOrWhiteSpace($config.pack.$Key)) {
                Write-Notice "Fudgefile does not contain a nuspec pack file for '$($Key)'"
                return
            }
        }

        # check packages
        elseif ($packageActions -icontains $Action)
        {
            if ((Test-Empty $config.packages) -and (!$Dev -or ($Dev -and (Test-Empty $config.devPackages)))) {
                Write-Notice "There are no packages to $($Action)"
                return
            }

            if ($DevOnly -and (Test-Empty $config.devPackages)) {
                Write-Notice "There are no devPackages to $($Action)"
                return
            }
        }
    }


    # check to see if chocolatey is installed
    if ($isChocoAction) {
        $isChocoInstalled = Test-Chocolatey
    }


    # check if the console is elevated (only needs to be done for certain actions)
    $isAdminAction = @('list', 'search', 'new', 'delete', 'renew', 'which', 'add', 'remove', 'pack') -inotcontains $Action
    $actionNeedsAdmin = (@('delete', 'remove') -icontains $Action -and $Uninstall) -or (@('new', 'renew', 'add') -icontains $Action -and $Install)

    if (((!$isChocoInstalled -and $isChocoAction) -or $isAdminAction -or $actionNeedsAdmin) -and !(Test-AdminUser))
    {
        Write-Notice 'Must be running with administrator privileges for Fudge to fully function'
        return
    }


    # if chocolatey isn't installed, install it
    if (!$isChocoInstalled -and $isChocoAction) {
        Install-Chocolatey
    }


    # if we are using a global custom source, output it for info
    if (!(Test-Empty $Source)) {
        Write-Notice "Source: $($Source)"
    }

    Write-Host ([string]::Empty)


    # retrieve a local list of what's currently installed
    if ($isChocoAction) {
        $localList = Get-ChocolateyLocalList
    }


    # invoke chocolatey based on the action required
    switch ($Action)
    {
        {($_ -ieq 'install') -or ($_ -ieq 'uninstall') -or ($_ -ieq 'upgrade')  -or ($_ -ieq 'downgrade')}
            {
                Invoke-ChocolateyAction -Action $Action -Key $Key -Source $Source -Config $config -LocalList $localList `
                    -Parameters $Parameters -Arguments $Arguments -Dev:$Dev -DevOnly:$DevOnly -Adhoc:$Adhoc
            }

        {($_ -ieq 'reinstall')}
            {
                Invoke-ChocolateyAction -Action 'uninstall' -Key $Key -Source $Source -Config $config -LocalList $localList `
                    -Parameters $Parameters -Arguments $Arguments -Dev:$Dev -DevOnly:$DevOnly -Adhoc:$Adhoc

                Invoke-ChocolateyAction -Action 'install' -Key $Key -Source $Source -Config $config -LocalList $localList `
                    -Parameters $Parameters -Arguments $Arguments -Dev:$Dev -DevOnly:$DevOnly -Adhoc:$Adhoc
            }

        {($_ -ieq 'pack')}
            {
                Invoke-ChocolateyAction -Action 'pack' -Key $Key -Config $config
            }

        {($_ -ieq 'list')}
            {
                Invoke-FudgeLocalDetails -Config $config -Key $Key -LocalList $localList -Dev:$Dev -DevOnly:$DevOnly
            }

        {($_ -ieq 'search')}
            {
                Invoke-Search -Key $Key -Limit $Limit -Source $Source -LocalList $localList
            }

        {($_ -ieq 'new')}
            {
                New-Fudgefile -Path $FudgefilePath -Key $Key -LocalList $localList -Install:$Install -Dev:$Dev -DevOnly:$DevOnly
            }

        {($_ -ieq 'renew')}
            {
                Restore-Fudgefile -Path $FudgefilePath -Key $Key -LocalList $localList -Install:$Install -Uninstall:$Uninstall -Dev:$Dev -DevOnly:$DevOnly
            }

        {($_ -ieq 'delete')}
            {
                Remove-Fudgefile -Path $FudgefilePath -Uninstall:$Uninstall -Dev:$Dev -DevOnly:$DevOnly
            }

        {($_ -ieq 'prune')}
            {
                Invoke-FudgePrune -Config $config -LocalList $localList -Dev:$Dev -DevOnly:$DevOnly
            }

        {($_ -ieq 'clean')}
            {
                Invoke-FudgeClean -LocalList $localList
            }

        {($_ -ieq 'add')}
            {
                Invoke-FudgeAdd -Path $FudgefilePath -Key $Key -Source $Source -Config $config -LocalList $localList `
                    -Parameters $Parameters -Arguments $Arguments -Dev:$Dev -Install:$Install
            }

        {($_ -ieq 'remove')}
            {
                Invoke-FudgeRemove -Path $FudgefilePath -Key $Key -Config $config -LocalList $localList `
                    -Parameters $Parameters -Arguments $Arguments -Dev:$Dev -Uninstall:$Uninstall
            }

        {($_ -ieq 'which')}
            {
                Invoke-FudgeWhich -Key $Key
            }

        {($_ -ieq 'rebuild')}
            {
                Invoke-FudgeClean -LocalList $localList
                Invoke-ChocolateyAction -Action 'install' -Key $Key -Source $Source -Config $config -Dev:$Dev -DevOnly:$DevOnly
            }

        default
            {
                Write-Fail "Action not recognised: $($_)"
            }
    }
}
finally
{
    # output duration, and cleanup
    Write-Details "`nDuration: $(([DateTime]::UtcNow - $timer).ToString())"
    Remove-Module -Name 'FudgeTools' -ErrorAction SilentlyContinue | Out-Null
}