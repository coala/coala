if (!($env:FudgeCI)) {
    if (Test-Path 'assets/fudge/FudgeCI.ps1') {
        $env:FudgeCI = 'assets/fudge/'
    }
    elseif (Test-Path '.ci/FudgeCI.ps1') {
        $env:FudgeCI = '.ci/'
    }
}

. $env:FudgeCI/PrepareAVVM.ps1

Set-StrictMode -Version latest

function Initialize-MinGW {
    # TODO: Handle versions other than 8.1.0
    Move-Item C:\mingw-w64\x86_64-8.1.0-posix-seh-rt_v6-rev0\mingw64 C:\MinGW81-x64
}

function Initialize-AppVeyorPreinstalledProduct {
    param(
        [array]
        $packages
    )

    foreach ($pkg in $packages) {
        $name = $pkg.Name

        $product = $pkg.AppVeyor_ID
        if ($product -eq $true) {
            Write-Information "No version choices available for AppVeyor $name"
            continue
        }

        $version = $pkg.Version

        $version_parts = ($version.Split('.'))

        if (!($env:AppVeyor)) {
            Write-Verbose "AppVeyor not set; skipping $product $version_parts"
            continue
        }

        if ($product -eq 'jdk') {
            # 8 -> 1.8.0
            $version = "1." + $version_parts[0] + ".0"
        }
        elseif ($product -eq 'MinGW') {
            Initialize-MinGW
        }
        elseif ($product -eq 'miniconda') {
            # TODO improve translation of real miniconda versions
            # into AppVeyor versions which are the python version
            if ($version -eq '4.5.12') {
                $version = '3.7'
            }

            if ($version[0] -eq '2') {
                Initialize-Miniconda27
            }
        }

        # Allow the installed version of python to be over
        if ($product -eq 'python') {
            if ($env:PYTHON_VERSION) {
                $version = $env:PYTHON_VERSION
            }
        }

        Add-Product $product $version $env:PLATFORM
        if (Test-Path "C:\avvm\$product\$version\$env:PLATFORM") {
            Install-Product $product $version $env:PLATFORM
        }
        elseif (Test-Path "C:\avvm\$product\$version") {
            if ($env:PLATFORM -eq 'x86') {
                $platform = 'x64'
            }
            else {
                $platform = 'x86'
            }
            Install-Product $product $version $platform
        }
    }
}

function Initialize-AppVeyorFakeChocoPackage {
    param(
        [array]
        $packages
    )

    New-Item -ItemType Directory -Force ($env:FudgeCI + '\\nuspecs\\') > $null

    Remove-Item "$env:FudgeCI/nuspecs/*.nupkg" -Force > $null

    foreach ($pkg in $packages) {
        . $env:FudgeCI/FudgeGenerateFake.ps1

        GenerateFakeNuspec $pkg.Name $pkg.Version

        $name = $pkg.Name

        $pkg.Source = "$env:FudgeCI/nuspecs/"

        $filename = "$env:FudgeCI/nuspecs/$name.nuspec"

        Invoke-Chocolatey -Action pack -Package $pkg.Name -Version $filename
    }
}

function Get-Preinstalled {
    try {
        if ($config) { }
    }
    catch {
        $config = Get-Content Fudgefile |
            ConvertFrom-Json
    }

    $appveyor_preinstalled = New-Object System.Collections.ArrayList

    foreach ($pkg in $config.packages) {
        try {
            if ($pkg.AppVeyor_ID) {
                $appveyor_preinstalled.Add($pkg) > $null
            }
        }
        catch {
            continue
        }
    }

    $appveyor_preinstalled
}

function Initialize-AppVeyorVM {
    $appveyor_preinstalled = Get-Preinstalled

    if (!($env:AppVeyor)) {
        Write-Notice "Not running on AppVeyor; skipping"
        return
    }

    Initialize-AppVeyorProductVersion

    Initialize-AppVeyorPreinstalledProduct $appveyor_preinstalled
}

function Invoke-FudgeAppVeyor {
    $appveyor_preinstalled = Get-Preinstalled

    if (!($env:AppVeyor)) {
        Write-Notice "Not running on AppVeyor; skipping"
        return
    }

    Initialize-AppVeyorFakeChocoPackage $appveyor_preinstalled
}

function Repair-Config {
    foreach ($pkg in $config.packages) {
        if (!($pkg.Source)) {
            $pkg.Source = $config.Source
        }
    }
}

function Invoke-FudgeCI {
    if (!($env:CI)) {
        Fix-Config

        Write-Notice "Not running on CI; skipping"
        return
    }

    Invoke-FudgeAppVeyor

    Repair-Config
}

$old_EAP = $ErrorActionPreference
$ErrorActionPreference = 'SilentlyContinue';
Export-ModuleMember -Function Prepare-AppVeyor-AVVM, Invoke-FudgeCI
$ErrorActionPreference = $old_EAP;
