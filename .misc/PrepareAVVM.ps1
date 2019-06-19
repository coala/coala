Set-StrictMode -Version latest

$PACKAGES_ROOT = "$env:SYSTEMDRIVE\avvm"
$REGISTRY_ROOT = 'HKLM:\Software\AppVeyor\VersionManager'

# GetInstalledProductVersion and Get-Version are copied from AVVM.ps1
function GetInstalledProductVersion ($product) {
    $productRegPath = "$REGISTRY_ROOT\$product"
    if (Test-Path $productRegPath) {
        $ver = Get-ItemProperty -Path $productRegPath
        @{
            Product = $product
            version = $ver.version
            Platform = $ver.Platform
        }
    }
}

function Get-Version ([string]$str) {
    $versionDigits = $str.Split('.')
    $version = @{
        major = -1
        minor = -1
        build = -1
        revision = -1
        number = 0
        value = $null
    }

    $version.value = $str

    if ($versionDigits -and $versionDigits.Length -gt 0) {
        $version.major = [int]$versionDigits[0]
    }
    if ($versionDigits.Length -gt 1) {
        $version.minor = [int]$versionDigits[1]
    }
    if ($versionDigits.Length -gt 2) {
        $version.build = [int]$versionDigits[2]
    }
    if ($versionDigits.Length -gt 3) {
        $version.revision = [int]$versionDigits[3]
    }

    for ($i = 0; $i -lt $versionDigits.Length; $i++) {
        $version.number += [long]$versionDigits[$i] -shl 16 * (3 - $i)
    }

    return $version
}

function SetInstalledProductVersion {
    param(
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $product,

        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $version,

        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $platform
    )

    $productRegPath = "$REGISTRY_ROOT\$product"
    New-Item $productRegPath -Force |
        Out-Null

    New-ItemProperty -Path $productRegPath -Name Version -PropertyType String -Value $version -Force |
        Out-Null

    New-ItemProperty -Path $productRegPath -Name Platform -PropertyType String -Value $platform -Force |
        Out-Null

    Write-Output "Creating $PACKAGES_ROOT\$product\$version\$platform"

    if (!(Test-Path "$PACKAGES_ROOT\$product\$version\$platform")) {
        New-Item -ItemType Directory "$PACKAGES_ROOT\$product\$version\$platform" -Force > $null
    }

    if (!(Test-Path "$PACKAGES_ROOT\$product\$version\$platform")) {
        throw "Something went wrong"
    }
}

function Add-Product {
    param(
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $product,

        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $version,

        [string]
        $platform
    )

    $name = $product

    if (!$platform) {
        $platform = $env:platform
    }

    $installed = GetInstalledProductVersion $Product

    $in_program_files = $false

    $version_parts = Get-Version $version

    if (($product -eq 'jdk') -or ($product -eq 'node')) {
        $in_program_files = $true

        if (($product -eq 'jdk') -and ($version_parts.minor -gt 8)) {
            # 1.9.0 -> 9
            $shortver = $version_parts.minor
        }
        else {
            $shortver = $version
        }

        if ($platform -eq 'x86') {
            $dir_name = "Program Files (x86)"
        }
        else {
            $dir_name = "Program Files"
        }
        if ($product -eq 'jdk') {
            $dir_name = "$dir_name\Java"
        }
        $dir_name = "$dir_name\$name"
    }
    else {
        $shortver = "{0}{1}" -f ($version_parts.major, $version_parts.minor)
        $dir_name = $name
    }


    if (Test-Path "$PACKAGES_ROOT\$name\$version\") {
        Write-Output "$PACKAGES_ROOT\$name\$version exists; skipping"

        if ($product -eq 'node') {
            $base = 'https://appveyordownloads.blob.core.windows.net/avvm'
            $versions_content = (New-Object Net.WebClient).DownloadString("$base/$name-versions.txt")
            Set-Content "$PACKAGES_ROOT\$name-versions.txt" $versions_content
            return
        }
    }

    if ($installed) {
        $current_version = $installed.version
        if ((Get-Version $current_version).number -gt $version_parts.number) {
            $versions_content = "$current_version
$version
lts:$version
stable:$version
current:$current_version
"
        }
        else {
            $versions_content = "$version
$current_version
lts:$version
stable:$version
current:$current_version
"
        }
    }
    else {
        $versions_content = "$version
lts:$version
stable:$version
"
    }
    Set-Content "$PACKAGES_ROOT\$name-versions.txt" $versions_content

    Write-Output "Wrote $PACKAGES_ROOT\$name-versions.txt"

    if ($product -eq 'MinGW') {
        if (Test-Path C:\avvm\MinGW) {
            # This is only needed for 5.3.0 x86, only vs2015 image
            Write-Output "Deleting pre-existing C:\avvm\MinGW ..."
            Remove-Item C:\avvm\MinGW
        }
    }

    if ($installed) {
        if ($installed.version -eq $version) {
            if ($installed.Platform -eq $platform) {
                Write-Output "$product $version $env:platform already set up"
                return;
            }
        }
    }

    New-Item -ItemType Directory "$PACKAGES_ROOT\$name" -Force > $null

    New-Item -ItemType Directory "$PACKAGES_ROOT\$name\$version" -Force > $null

    Write-Verbose "Looking for C:\$dir_name$shortver .."

    if (!(Test-Path "C:\$dir_name$shortver")) {
        if (!(Test-Path "C:\$dir_name$shortver-x64")) {
            throw "Cant find $dir_name$shortver or C:\$dir_name$shortver-x64"
        }

        # Use x64 if x86 not available
        $platform = 'x64'
    }

    New-Item -ItemType Directory "$PACKAGES_ROOT\$name\$version\$platform" -Force > $null

    if ($in_program_files) {
        $dir = "C:\$dir_name$shortver"
    }
    else {
        Write-Output "Looking for C:\$name$shortver-x64 .."

        $dir = ''
        if (Test-Path "C:\$dir_name$shortver-x64") {
            if ($platform -eq "x64") {
                $dir = "C:\$dir_name$shortver-x64"
            }
            else {
                $dir = "C:\$dir_name$shortver"
            }
        }

        # TODO: Re-arrange to look only for the needed platform
        if (!$dir) {
            Write-Output "Looking for C:\$dir_name$shortver-x86 .."
        }

        if ((!($dir)) -and (Test-Path "C:\$dir_name$shortver-x86")) {
            if ($platform -eq "x86") {
                $dir = "C:\$dir_name$shortver-x86"
            }
            else {
                $dir = "C:\$dir_name$shortver"
            }
        }
    }

    if (!($dir)) {
        throw 'couldnt find x86/x64 directories for $name'
    }

    if (!(Test-Path $dir)) {
        throw "Cant find $dir"
    }

    Write-Output "Coping $dir to $PACKAGES_ROOT\$name\$version\$platform\$name ..."

    Move-Item $dir "$PACKAGES_ROOT\$name\$version\$platform\$name"

    $files_content = ('$files = @{ "' + $name + '" = "C:\' + $name + '" }')
    $files_path = "$PACKAGES_ROOT\$name\$version\$platform\files.ps1"

    Set-Content $files_path $files_content

    Write-Output "Wrote $files_path"
}

function Initialize-Miniconda27 {
    # The algorithm above to prepare products for switching depends on a version
    # in the directory name, which works for all cases except for Miniconda27.
    # Use this if you need Miniconda27.
    Write-Output "Moving C:\Miniconda(-x64) to C:\Miniconda27(-x64)"
    Move-Item C:\Miniconda C:\Miniconda27
    Move-Item C:\Miniconda-x64 C:\Miniconda27-x64
}

function Initialize-AppVeyorProductVersion {
    # TODO: Only set up default versions for products which are needed

    # This tells Install-Product to load product versions from $PACKAGES_ROOT
    $env:AVVM_DOWNLOAD_URL = '../../avvm/'
    Set-ItemProperty -Path 'HKCU:\Environment' -Name 'AVVM_DOWNLOAD_URL' -Value $env:AVVM_DOWNLOAD_URL

    # node already set to 8.x
    SetInstalledProductVersion go 1.12.3 x64

    # todo: Handle Python27 and Ruby193

    SetInstalledProductVersion miniconda 2.7.15 x86
    SetInstalledProductVersion miniconda3 3.7.0 x86

    SetInstalledProductVersion jdk 1.6.0 x86
    SetInstalledProductVersion perl 5.20.1 x86
    # /C/MinGW is only set on vs2013 and vs2015 images, and it isnt desirable
    # SetInstalledProductVersion MinGW 5.3.0 x86

    # hg 4.1.1 is pre-installed, but it does not need to be replaced,
    # and is instead reported as 5.0
}

$old_EAP = $ErrorActionPreference
$ErrorActionPreference = 'SilentlyContinue';
Export-ModuleMember -Function Initialize-AppVeyorProductVersion, Add-Product, Initialize-Miniconda27
$ErrorActionPreference = $old_EAP;
