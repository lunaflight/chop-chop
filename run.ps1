# Stop on first error
$ErrorActionPreference = "Stop"

# set utf-8
chcp 65001 > $null
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8

# Go to directory
Set-Location -Path $PSScriptRoot

## Script to run main.py in Powershell
# Accepts multiple comma-separated URLs, concatenated together and automatically copied to clipboard.

# Create virtual environment if not exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
	# Activate venv
	Write-Host "Activating virtual environment..."
	& "$PSScriptRoot\venv\Scripts\Activate.ps1"
	# Install dependencies
	Write-Host "Installing dependencies..."
	pip install -r requirements.txt
} else {
	# Activate venv
	Write-Host "Activating virtual environment..."
	& "$PSScriptRoot\venv\Scripts\Activate.ps1"
}

# Loop main.py so can keep pasting new inputs
while ($true) {
	Write-Host "`Paste one or more valid permalink URLs (comma-separated) here (or type 'x' to quit):"
	$inputLine = Read-Host

	if ($inputLine -eq "x") { break }
	
	# Split inputs by comma, trim spaces
    $urls = $inputLine -split "," | ForEach-Object { $_.Trim() }
	
	$outputs = @()  # array for outputs

	foreach ($url in $urls) {
		if ($url -eq "") { continue }
		
		try {
			$output = [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
			$output = python -m src.main <<< $url
			
			# Copy to clipboard
			Write-Host "Output:" -ForegroundColor Yellow
			Write-Host $output  -ForegroundColor Black -BackgroundColor Yellow
			
			# Add to outputs array as JSON
			$outputs += $output.Trim()
		} catch {
			Write-Host "`n❌ Error running script:"
			Write-Host $_
		}
	}
	
	if ($outputs.Count -gt 0) {
		# Concatenate outputs
		$jsonOutput = $outputs -join ",`n"
	}
	
	# Copy to clipboard
	$jsonOutput | Set-Clipboard
	Write-Host "JSON copied to clipboard!" -ForegroundColor Green
}

Write-Host "`nAll outputs processed. Paste more URLs here (or type 'x' to quit):" -ForegroundColor Green

# Deactivate venv when done
deactivate
Write-Host "`nDone! Press Enter to exit." -ForegroundColor Magenta
Read-Host