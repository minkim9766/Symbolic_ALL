function Invoke-SymbolicAll {
    [CmdletBinding()]
    param (
        [Parameter(Position = 0)]
        [string]$SourcePath = (Get-Location).Path,

        [Parameter(Mandatory = $true, Position = 1)]
        [string]$TargetPath
    )

    $SourcePath = (Resolve-Path -Path $SourcePath).Path

    if (!(Test-Path -Path $TargetPath)) {
        New-Item -ItemType Directory -Path $TargetPath | Out-Null
    }

    Get-ChildItem -Path $SourcePath -Force | ForEach-Object {
        $linkPath = Join-Path -Path $TargetPath -ChildPath $_.Name
        $sourceItem = $_.FullName

        if ($_.PSIsContainer) {
            cmd /c mklink /D "`"$linkPath`"" "`"$sourceItem`"" | Out-Null
        } else {
            cmd /c mklink "`"$linkPath`"" "`"$sourceItem`"" | Out-Null
        }
    }
}
