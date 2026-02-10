$ErrorActionPreference = 'SilentlyContinue'
$project = 'C:\IA\Quatuors'
$port = 8123

while (([System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners().Port) -contains $port) {
    $port++
}

$cmd = "cd /d `"$project`" && (py -3 server.py $port || python server.py $port)"
Start-Process -FilePath 'cmd.exe' -ArgumentList '/k', $cmd -WorkingDirectory $project
Start-Sleep -Seconds 2
Start-Process "http://localhost:$port/index.html"
