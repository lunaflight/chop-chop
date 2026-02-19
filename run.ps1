try {
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

if (-not (Test-Path "venv")) {
	Write-Host "Creating virtual environment..."
    python -m venv venv
}
Write-Host "Activating virtual environment..."
& "$PSScriptRoot\venv\Scripts\Activate.ps1"

Write-Host "Installing dependencies..."
pip install -r requirements.txt

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
			# Read full Python stdout as ONE SINGLE STRING
			$output = $url | python -m src.main | Out-String
			$output = $output.Trim()
			
			# Copy to clipboard
			Write-Host "Output:" -ForegroundColor Yellow
			Write-Host $output  -ForegroundColor Black -BackgroundColor Yellow
			
			# Add to outputs array as JSON
			if ($output -and $output.Trim() -ne "") {
				$outputs += $output.Trim()
			}
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
    Set-Clipboard -Value $jsonOutput

    Write-Host "JSON copied to clipboard!" -ForegroundColor Green
}

Write-Host "`nAll outputs processed. Paste more URLs here (or type 'x' to quit):" -ForegroundColor Green

# Deactivate venv when done
deactivate
Write-Host "`nDone! Press Enter to exit." -ForegroundColor Magenta
Read-Host
} catch {
    Write-Host "Unhandled error: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}