<#
Windows repair script for ProjectSynapse
- Installs Python requirements in backend
- Installs pytest
- Runs tests
- Runs the AI debugger in diagnose mode
#>
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$Root = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Write-Host "Workspace root: $Root"

# Use conda-run if available (configured earlier). Otherwise use system python.
$condaExe = "C:/Users/user/miniconda3/Scripts/conda.exe"
$backend = Join-Path $Root "ProjectSynapse\backend"

function Invoke-Python {
    param([string[]]$PythonArgs)
    # Prevent accidental interactive REPL: if no args are passed, run a no-op command.
    if (-not $PythonArgs -or $PythonArgs.Count -eq 0) {
        $PythonArgs = @('-c', 'print("(no-op)")')
    }
    if (Test-Path $condaExe) {
        & $condaExe run -p C:\Users\user\miniconda3 --no-capture-output python @PythonArgs
    } else {
        python @PythonArgs
    }
}

Push-Location $backend
try {
    if (Test-Path requirements.txt) {
        Write-Host "Installing backend requirements..."
    Invoke-Python -PythonArgs @("-m","pip","install","-r","requirements.txt")
    } else {
        Write-Host "No requirements.txt in backend"
    }

    Write-Host "Ensuring pytest is installed..."
    Invoke-Python -PythonArgs @("-m","pip","install","pytest")

    Write-Host "Running pytest..."
    if (Test-Path "$env:CONDA_DEFAULT_ENV") {
        & pytest -q
    } else {
        Invoke-Python -PythonArgs @("-m","pytest","-q")
    }

    Write-Host "Running AI debugger (diagnose)..."
    Invoke-Python -PythonArgs @("tools\\ai_debugger.py","--diagnose","--report")
} finally {
    Pop-Location
}

Write-Host "Repair script finished."
