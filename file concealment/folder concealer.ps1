# Define the path to the JSON file
$jsonFilePath = "C:\Users\Bafana\PycharmProjects\File Manager\config\folder paths.JSON"

# Read the content of the JSON file and convert it to a PowerShell object
$jsonContent = Get-Content -Path $jsonFilePath -Raw | ConvertFrom-Json

# Now you can work with $jsonContent as a PowerShell object
$jsonContent

#Get-ChildItem -Path C:\ -Force