# Define the path to the JSON file
#$jsonFilePath = "C:\Users\Bafana\PycharmProjects\File Manager\config\folder_paths.JSON"
#$jsonFilePath = Join-Path (Get-Location).Path "config\folder_paths.json"
$jsonFilePath = Join-Path $PSScriptRoot "config\folder_paths.json"

try {
    $jsonFilePath = Join-Path $PSScriptRoot "config\folder_paths.json"
    $jsonContent = Get-Content -Path $jsonFilePath -Raw | ConvertFrom-Json

    # Rest of your script
} catch [System.IO.FileNotFoundException] {
    Write-Warning "JSON file not found: $jsonFilePath"
    # Handle the error, e.g., provide default values or exit the script
}


# Read the content of the JSON file and convert it to a PowerShell object
# $jsonContent = Get-Content -Path $jsonFilePath -Raw | ConvertFrom-Json


foreach ($folder in $jsonContent.hidden_folders) {
    Get-ChildItem $folder -Recurse | ForEach-Object { $_.Attributes = $_.Attributes -bor [System.IO.FileAttributes]::Hidden }
    attrib +h $folder
}

reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v Hidden /t REG_DWORD /d 2 /f
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v ShowSuperHidden /t REG_DWORD /d 0 /f
#powershell -c gps 'explorer' ^| stop-process

# no no