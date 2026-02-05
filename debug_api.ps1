# Debug script - shows FULL response
$apiUrl = "https://voice-detection-api-c1j5.onrender.com/detect"
$apiKey = "hackathon-voice-detection-key-2026"
$sampleAudio = "SUQzBAAAAAECBVRTU0UAAAAOAAADTGF2ZjYwLjE2LjEwMA=="

$headers = @{
    "Content-Type" = "application/json"
    "X-API-Key" = $apiKey
}

$body = @{
    audio = $sampleAudio
} | ConvertTo-Json

Write-Host "Sending request..." -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri $apiUrl -Method Post -Headers $headers -Body $body
    
    Write-Host "`n=== FULL RESPONSE ===" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)
    
    Write-Host "`n=== RESPONSE TYPE ===" -ForegroundColor Cyan
    Write-Host $response.GetType().FullName
    
    Write-Host "`n=== PROPERTIES ===" -ForegroundColor Cyan
    $response | Get-Member -MemberType Properties | Format-Table
    
    Write-Host "`n=== VALUES ===" -ForegroundColor Cyan
    foreach ($prop in $response.PSObject.Properties) {
        Write-Host "$($prop.Name): $($prop.Value)"
    }
    
} catch {
    Write-Host "ERROR!" -ForegroundColor Red
    Write-Host "Status: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    Write-Host "Message: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Red
    }
}
