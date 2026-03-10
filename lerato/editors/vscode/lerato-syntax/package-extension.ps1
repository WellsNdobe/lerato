param(
    [string]$OutputDirectory = "."
)

$ErrorActionPreference = "Stop"

$extensionRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$packageJsonPath = Join-Path $extensionRoot "package.json"
$packageJson = Get-Content $packageJsonPath -Raw | ConvertFrom-Json

$publisher = [string]$packageJson.publisher
$extensionName = [string]$packageJson.name
$version = [string]$packageJson.version
$displayName = [string]$packageJson.displayName
$description = [string]$packageJson.description
$engineVersion = [string]$packageJson.engines.vscode
$categories = @($packageJson.categories)

if (-not $publisher -or -not $extensionName -or -not $version) {
    throw "package.json must define publisher, name, and version."
}

$normalizedEngineVersion = $engineVersion.TrimStart("^")
if (-not $normalizedEngineVersion) {
    $normalizedEngineVersion = "1.85.0"
}

$outputRoot = [System.IO.Path]::GetFullPath((Join-Path $extensionRoot $OutputDirectory))
New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null

$tempRoot = Join-Path $extensionRoot ".vsix-build"
$packageRoot = Join-Path $tempRoot "package"
$extensionPackageRoot = Join-Path $packageRoot "extension"

if (Test-Path $tempRoot) {
    Remove-Item -Recurse -Force $tempRoot
}

New-Item -ItemType Directory -Force -Path $extensionPackageRoot | Out-Null

$excludeNames = @(
    ".git",
    ".vsix-build",
    ".npm-cache",
    "node_modules",
    "*.vsix",
    "*.zip",
    "package-extension.ps1"
)

Get-ChildItem -Path $extensionRoot -Force | Where-Object {
    $entryName = $_.Name
    foreach ($pattern in $excludeNames) {
        if ($entryName -like $pattern) {
            return $false
        }
    }
    return $true
} | ForEach-Object {
    Copy-Item -Recurse -Force $_.FullName -Destination $extensionPackageRoot
}

$escapedDescription = [System.Security.SecurityElement]::Escape($description)
$escapedDisplayName = [System.Security.SecurityElement]::Escape($displayName)
$escapedPublisher = [System.Security.SecurityElement]::Escape($publisher)
$escapedIdentity = [System.Security.SecurityElement]::Escape("$publisher.$extensionName")
$escapedCategories = [System.Security.SecurityElement]::Escape(($categories -join ","))

$manifest = @"
<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011">
  <Metadata>
    <Identity Language="en-US" Id="$escapedIdentity" Version="$version" Publisher="$escapedPublisher" />
    <DisplayName>$escapedDisplayName</DisplayName>
    <Description xml:space="preserve">$escapedDescription</Description>
    <Categories>$escapedCategories</Categories>
  </Metadata>
  <Installation>
    <InstallationTarget Id="Microsoft.VisualStudio.Code" Version="[$normalizedEngineVersion,)" />
  </Installation>
  <Dependencies />
  <Assets>
    <Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true" />
    <Asset Type="Microsoft.VisualStudio.Services.Content.Details" Path="extension/README.md" Addressable="true" />
  </Assets>
</PackageManifest>
"@

$contentTypes = @"
<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="json" ContentType="application/json" />
  <Default Extension="md" ContentType="text/markdown" />
  <Default Extension="txt" ContentType="text/plain" />
  <Default Extension="vsixmanifest" ContentType="text/xml" />
</Types>
"@

$manifest | Out-File -FilePath (Join-Path $packageRoot "extension.vsixmanifest") -Encoding utf8
$contentTypes | Out-File -LiteralPath (Join-Path $packageRoot "[Content_Types].xml") -Encoding utf8

$vsixName = "$publisher.$extensionName-$version.vsix"
$zipPath = Join-Path $outputRoot "$publisher.$extensionName-$version.zip"
$vsixPath = Join-Path $outputRoot $vsixName

if (Test-Path $zipPath) {
    Remove-Item -Force $zipPath
}
if (Test-Path $vsixPath) {
    Remove-Item -Force $vsixPath
}

Compress-Archive -Path (Join-Path $packageRoot "*") -DestinationPath $zipPath -Force
Move-Item -Force $zipPath $vsixPath

Remove-Item -Recurse -Force $tempRoot

Write-Output "Created $vsixPath"
