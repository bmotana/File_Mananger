# Define the path to the JSON file
$jsonFilePath = "C:\Users\Bafana\PycharmProjects\File Manager\config\folder paths.JSON"

# Read the content of the JSON file and convert it to a PowerShell object
$jsonContent = Get-Content -Path $jsonFilePath -Raw | ConvertFrom-Json


foreach ($folder in $jsonContent.hidden_folders) {
    Get-ChildItem $folder -Recurse | ForEach-Object { $_.Attributes = $_.Attributes -bor [System.IO.FileAttributes]::Hidden }
    attrib +h $folder
}

reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v Hidden /t REG_DWORD /d 2 /f
reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced /v ShowSuperHidden /t REG_DWORD /d 0 /f
#powershell -c gps 'explorer' ^| stop-process

# no no