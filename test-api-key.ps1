# PowerShell script to test API keys
# Usage: .\test-api-key.ps1

Write-Host "🧪 API Key Test Script for Windows PowerShell" -ForegroundColor Cyan
Write-Host "=" -repeat 50

# Check if server is running
Write-Host "`n1. Checking if server is running..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Server is running!" -ForegroundColor Green
} catch {
    Write-Host "❌ Server is not running!" -ForegroundColor Red
    Write-Host "Please start the server first: python start.py" -ForegroundColor Yellow
    exit 1
}

# Prompt for API key
Write-Host "`n2. Testing API Key Authentication" -ForegroundColor Yellow
Write-Host "First, create an API key:" -ForegroundColor Cyan
Write-Host "   1. Visit: http://localhost:8000/login" -ForegroundColor White
Write-Host "   2. Then go to: http://localhost:8000/api/keys/manage" -ForegroundColor White
Write-Host "   3. Create a new API key and copy it" -ForegroundColor White

$apiKey = Read-Host "`nPaste your API key here (or press Enter to skip)"

if ([string]::IsNullOrWhiteSpace($apiKey)) {
    Write-Host "`n⚠️  No API key provided. Exiting." -ForegroundColor Yellow
    exit 0
}

# Test the API key
Write-Host "`n3. Testing API key: $($apiKey.Substring(0, [Math]::Min(15, $apiKey.Length)))..." -ForegroundColor Yellow

try {
    $headers = @{
        "X-API-Key" = $apiKey
    }
    
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/keys/test" -Headers $headers -Method GET
    $data = $response.Content | ConvertFrom-Json
    
    Write-Host "`n✅ API Key is VALID!" -ForegroundColor Green
    Write-Host "User: $($data.user_email)" -ForegroundColor Cyan
    Write-Host "Message: $($data.message)" -ForegroundColor Cyan
    Write-Host "`nFull Response:" -ForegroundColor Yellow
    $data | ConvertTo-Json -Depth 3 | Write-Host
    
} catch {
    Write-Host "`n❌ API Key test FAILED!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "Status Code: $statusCode" -ForegroundColor Yellow
        
        if ($statusCode -eq 401) {
            Write-Host "`nPossible reasons:" -ForegroundColor Yellow
            Write-Host "  - Invalid API key" -ForegroundColor White
            Write-Host "  - Expired API key" -ForegroundColor White
            Write-Host "  - Revoked API key" -ForegroundColor White
        }
    }
}

Write-Host "`n" -NoNewline
Read-Host "Press Enter to exit"
