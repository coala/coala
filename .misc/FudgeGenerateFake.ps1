Set-StrictMode -Version latest

$template = @'
<?xml version="1.0"?>
<package xmlns="http://schemas.microsoft.com/packaging/2010/07/nuspec.xsd">
  <metadata>
    <id>{name}</id>
    <version>{version}</version>
    <title>{name} {version}</title>
    <authors>AppVeyor</authors>
    <description>Fake generated {name} package to fulfil dependencies.</description>
    <dependencies>
      <dependency id="chocolatey"/>
    </dependencies>
  </metadata>
</package>
'@

function GenerateFakeNuspec {
    param(
        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $name,

        [Parameter(Mandatory = $true)]
        [ValidateNotNullOrEmpty()]
        [string]
        $version
    )

    $content = $template -replace '{name}', $name
    $content = $content -replace '{version}', $version

    $nuspec = ($env:FudgeCI + '\nuspecs\' + $name + '.nuspec')

    Set-Content $nuspec $content

    Write-Output "Created $nuspec"
}

Export-ModuleMember -Function GenerateFakeNuspec
