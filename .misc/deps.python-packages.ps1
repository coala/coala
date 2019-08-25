$ci_directory = $env:FudgeCI

if (!($ci_directory)) {
    $ci_directory = '.ci'
}

. $ci_directory/constants.ps1

function Checkpoint-Pip-Constraints {
    python -m pip freeze --all > constraints.txt
}

function Install-Pip-Requirement {
    param (
        [parameter(Mandatory, ValueFromPipeline)]
        [string]
        $requirement
    )

    if ($requirement.EndsWith('.txt')) {
        python -m pip install --constraint constraints.txt --constraint test-requirements.txt -r $requirement
    }
    else {
        python -m pip install --constraint constraints.txt --constraint test-requirements.txt $requirement.Split()
    }
}

function Install-Binary-Packages {
    # Install lxml needed by for coala-bears as a wheel as libxml2 and libxslt
    # headers and library files are not available, and STATIC_DEPS=true often
    # results in linter problems due to different VS compilers and MS runtimes.
    # Also use cffi wheel to avoid need for VS compilers
    python -m pip install --prefer-binary cffi lxml
    # pycparser not a wheel, but ensure it is installable before proceeding
    # https://github.com/eliben/pycparser/issues/251
    python -m pip --verbose install pycparser
}

function Install-coala {
    param (
        [string]
        $stop_at
    )

    python -m pip install -U six pip==$pip_version setuptools==$setuptools_version

    if (!(Test-Path constraints.txt)) {
        if ($stop_at -eq 'coala-bears') {
            cp bear-requirements.txt constraints.txt
        }
        elseif (Test-Path 'requirements.txt') {
            cp requirements.txt constraints.txt
        }
        else {
            Checkpoint-Pip-Constraints
        }

        # pip bales on encountering VCS or other imprecise requirements
        sed -Ei '/(git|hg)+/d' constraints.txt
    }

    if (!($stop_at -eq 'PyPrint')) {
        Write-Output "Installing PyPrint"
        Install-Pip-Requirement 'git+https://gitlab.com/coala/PyPrint#egg=PyPrint'

        if (!($stop_at -eq 'coala_utils')) {
            Write-Output "Installing coala_utils"

            Checkpoint-Pip-Constraints

            Install-Pip-Requirement 'git+https://gitlab.com/coala/coala-utils#egg=coala-utils'

            if (!($stop_at -eq 'dependency-management')) {
                Write-Output "Installing sarge with Windows support"

                Install-Pip-Requirement 'hg+https://bitbucket.org/jayvdb/sarge@win-reg-lookup#egg=sarge'

                if (!(Test-Path $env:TEMP/pm-master)) {
                    $PM_URL = "https://gitlab.com/coala/package_manager.git/"
                    git clone $PM_URL $env:TEMP/pm-master
                }
                rm $env:TEMP/pm-master/test-requirements.txt
                rm $env:TEMP/pm-master/requirements.txt
                touch $env:TEMP/pm-master/test-requirements.txt
                touch $env:TEMP/pm-master/requirements.txt

                Install-Pip-Requirement "$env:TEMP/pm-master"

                if (!($stop_at -eq 'coala')) {
                    Write-Output "Installing coala"

                    Checkpoint-Pip-Constraints

                    Install-Pip-Requirement 'git+https://github.com/coala/coala#egg=coala'

                    if (!($stop_at -eq 'coala-bears')) {
                        Write-Output "Installing coala-bears"

                        Checkpoint-Pip-Constraints

                        Install-Pip-Requirement 'git+https://github.com/coala/coala-bears#egg=coala-bears'
                    }
                }
            }
        }
    }
}

function Install-Project-Dependency-Packages {
    Write-Output "Installing dependencies of $project_name"
    Install-coala $project_name
}

function Install-Project {
    if (Test-Path 'requirements.txt') {
        Write-Output "Installing $project_name requirements.txt"

        Install-Pip-Requirement 'requirements.txt'
    }

    if (Test-Path 'setup.py') {
        Write-Output "Installing $project_name setup.py"
        Install-Pip-Requirement '.'
    }

    # coala-bears has an ignore.txt for optional dependencies that ordinary
    # users may be unable to install.  They are needed to reach 100% coverage.
    if (Test-Path 'ignore.txt') {
        Install-Pip-Requirement 'ignore.txt'
    }
}

function Install-Test-Packages {
    if (Test-Path docs-requirements.txt) {
        Write-Output "Installing docs-requirements.txt"

        Checkpoint-Pip-Constraints

        Install-Pip-Requirement 'docs-requirements.txt'
    }

    Checkpoint-Pip-Constraints

    Write-Output "Installing test-requirements.txt"

    Install-Pip-Requirement 'test-requirements.txt'
    Install-Pip-Requirement 'pytest-spec'

    if ($project_name -eq 'coala-bears') {
        Write-Output "Installing tox"
        # Avoid previous cache entry for setuptools, as it
        # causes a deserialisation error
        python -m pip install -U --no-cache-dir setuptools

        Checkpoint-Pip-Constraints

        # tox 3.13 uses pluggy 0.12.0 which is incompatible with a pytest 3.6.4
        Install-Pip-Requirement 'tox~=3.12.0 tox-backticks'
    }
}

function Invoke-ExtraInstallation {

    $old_pip_check_flag = 0
    if ($env:PIP_DISABLE_PIP_VERSION_CHECK) {
        $old_pip_check_flag = 1
    }
    $env:PIP_DISABLE_PIP_VERSION_CHECK = 1

    Install-Binary-Packages

    if (!($env:PYTHON_VERSION -eq '2.7')) {
        Install-Project-Dependency-Packages
    }

    Install-Project

    Install-Test-Packages

    if (Test-Path constraints.txt) {
        Move-Item constraints.txt $env:TEMP -Force
    }

    if (!$old_pip_check_flag) {
        Remove-Item Env:\PIP_DISABLE_PIP_VERSION_CHECK
    }
}

$ErrorActionPreference = 'SilentlyContinue';
Export-ModuleMember -Function Invoke-ExtraInstallation -ErrorAction:Ignore
$ErrorActionPreference = 'Continue';
