# Можно проверить на сетевой шаре версию клиента
# $clientVersion = 1

$computername = ((gwmi win32_computersystem -ErrorAction SilentlyContinue).name).toupper()

if($computername -eq $null){
    $wmiWarn  = 1
    $computername = ($env:COMPUTERNAME).toupper()
}else{
    $wmiWarn = 0
}

$date = Get-Date
$fileNameDate = [string]$date.Year+'_'+[string]$date.month+'_'+[string]$date.Day

#$outFile = "C:\programdata\"+$computername+".json"

$outFile = "\\dc08-fs-01\temp\allwsmonitor\"+$computername+"\"+$fileNameDate+".json"
if(test-path ("\\dc08-fs-01\temp\allwsmonitor\"+$computername+"\")){
}else{
    $tempoutvar = New-Item -ItemType Directory ("\\dc08-fs-01\temp\allwsmonitor\"+$computername+"\") -InformationAction SilentlyContinue
    Remove-Variable tempoutvar
}

# LD -- Last Day
########################### LogName System
$SysEvLDCrit = Get-WinEvent -FilterHashTable @{LogName='system'; Level=1; StartTime=((get-date).AddDays(-1))} -ErrorAction SilentlyContinue
$SysEvLDErr = Get-WinEvent -FilterHashTable @{LogName='system'; Level=2; StartTime=((get-date).AddDays(-1))} -ErrorAction SilentlyContinue
$SysEvLDWarn = Get-WinEvent -FilterHashTable @{LogName='system'; Level=3; StartTime=((get-date).AddDays(-1))} -ErrorAction SilentlyContinue
$SysEvLD_GroupCrit = $SysEvLDCrit | Group-Object -Property id -NoElement
$SysEvLD_GroupErr = $SysEvLDErr | Group-Object -Property id -NoElement
$SysEvLD_GroupWarn = $SysEvLDWarn | Group-Object -Property id -NoElement
# Warning processing
if($SysEvLD_GroupWarn -ne $null){
    $out_sys_warning = @{}
    foreach($events in $SysEvLD_GroupWarn){
        $e = @{}
        $event = Get-WinEvent -FilterHashTable @{LogName='system'; Level=3; id=$events.name; StartTime=((get-date).AddDays(-1))} -ErrorAction SilentlyContinue | Select-Object -First 1
        $e["count"] = $events.Count
        $e["id"] = $event.id
        $e["source"] = $event.ProviderName
        try{
            $e_user_sid = new-object System.Security.Principal.SecurityIdentifier(($event.userid).Value)
            $e["user"] = $e_user_sid.translate([System.Security.Principal.NTAccount]).value
        }
        catch{
            $e["user"] = "NA"
        }
        $e["description"] = $event.message
        # $e["logged"] = get-date $event.timecreated -Format o
        $e["machineName"] = $event.machineName
        $id_key = [string]($event.id)
        $out_sys_warning[$id_key] = $e
    }
}else{
    $out_sys_warning = 0
}
# Error processing
if($SysEvLD_GroupErr -ne $null){
    $out_sys_error = @{}
    foreach($events in $SysEvLD_GroupErr){
        $e = @{}
        $event = Get-WinEvent -FilterHashTable @{LogName='system'; Level=2; id=$events.name; StartTime=((get-date).AddDays(-1))} -ErrorAction SilentlyContinue | Select-Object -First 1
        $e["count"] = $events.Count
        $e["id"] = $event.id
        $e["source"] = $event.ProviderName
        try{
            $e_user_sid = new-object System.Security.Principal.SecurityIdentifier(($event.userid).Value)
            $e["user"] = $e_user_sid.translate([System.Security.Principal.NTAccount]).value}
        catch{
            $e["user"] = "NA"
        }
        $e["description"] = $event.message
        # $e["logged"] = get-date $event.timecreated -Format o
        $e["machineName"] = $event.machineName
        $id_key = [string]($event.id)
        $out_sys_error[$id_key] = $e
    }
}else{
    $out_sys_error = 0
}
# Critical processing
if($SysEvLD_GroupCrit -ne $null){
    $out_sys_critical = @{}
    foreach($events in $SysEvLD_GroupCrit){
        $e = @{}
        $event = Get-WinEvent -FilterHashTable @{LogName='system'; Level=1; id=$events.name; StartTime=((get-date).AddDays(-1))} -ErrorAction SilentlyContinue | Select-Object -First 1
        $e["count"] = $events.Count
        $e["id"] = $event.id
        $e["source"] = $event.ProviderName
        try{
            $e_user_sid = new-object System.Security.Principal.SecurityIdentifier(($event.userid).Value)
            $e["user"] = $e_user_sid.translate([System.Security.Principal.NTAccount]).value
        }
        catch{
            $e["user"] = "NA"
        }
        $e["description"] = $event.message
        # $e["logged"] = get-date $event.timecreated -Format o
        $e["machineName"] = $event.machineName
        $id_key = [string]($event.id)
        $out_sys_critical[$id_key] = $e
    }
}else{
    $out_sys_critical = 0
}

#################### LogName Application
$AppEvLDCrit = Get-WinEvent -FilterHashTable @{LogName='application'; Level=1; StartTime=((get-date).AddDays(-1))} -ErrorAction SilentlyContinue
$AppEvLDErr = Get-WinEvent -FilterHashTable @{LogName='application'; Level=2; StartTime=((get-date).AddDays(-1))} -ErrorAction SilentlyContinue
$AppEvLDWarn = Get-WinEvent -FilterHashTable @{LogName='application'; Level=3; StartTime=((get-date).AddDays(-1))} -ErrorAction SilentlyContinue
$AppEvLD_GroupCrit = $AppEvLDCrit | Group-Object -Property id -NoElement
$AppEvLD_GroupErr = $AppEvLDErr | Group-Object -Property id -NoElement
$AppEvLD_GroupWarn = $AppEvLDWarn | Group-Object -Property id -NoElement
# Warning processing
if($AppEvLD_GroupWarn -ne $null){
    $out_app_warning = @{}
    foreach($events in $AppEvLD_GroupWarn){
        $e = @{}
        $event = Get-WinEvent -FilterHashTable @{LogName='application'; Level=3; id=$events.name; StartTime=((get-date).AddDays(-1))} -ErrorAction SilentlyContinue | Select-Object -First 1
        $e["count"] = $events.Count
        $e["id"] = $event.id
        $e["source"] = $event.ProviderName
        try{
            $e_user_sid = new-object System.Security.Principal.SecurityIdentifier(($event.userid).Value)
            $e["user"] = $e_user_sid.translate([System.Security.Principal.NTAccount]).value
        }
        catch{
            $e["user"] = "NA"
        }
        $e["description"] = $event.message
        # $e["logged"] = get-date $event.timecreated -Format o
        $e["machineName"] = $event.machineName
        $id_key = [string]($event.id)
        $out_app_warning[$id_key] = $e
    }
}else{
    $out_app_warning = 0
}
# Error processing
if($AppEvLD_GroupErr -ne $null){
    $out_app_error = @{}
    foreach($events in $AppEvLD_GroupErr){
        $e = @{}
        $event = Get-WinEvent -FilterHashTable @{LogName='application'; Level=2; id=$events.name; StartTime=((get-date).AddDays(-1))} -ErrorAction SilentlyContinue | Select-Object -First 1
        $e["count"] = $events.Count
        $e["id"] = $event.id
        $e["source"] = $event.ProviderName
        try{
            $e_user_sid = new-object System.Security.Principal.SecurityIdentifier(($event.userid).Value)
            $e["user"] = $e_user_sid.translate([System.Security.Principal.NTAccount]).value
        }
        catch{$e["user"] = "NA"}
        $e["description"] = $event.message
        # $e["logged"] = get-date $event.timecreated -Format o
        $e["machineName"] = $event.machineName
        $id_key = [string]($event.id)
        $out_app_error[$id_key] = $e
    }
}else{
    $out_app_error = 0
}
# Critical processing
if($AppEvLD_GroupCrit -ne $null){
    $out_app_critical = @{}
    foreach($events in $AppEvLD_GroupCrit){
        $e = @{}
        $event = Get-WinEvent -FilterHashTable @{LogName='application'; Level=1; id=$events.name; StartTime=((get-date).AddDays(-1))} -ErrorAction SilentlyContinue | Select-Object -First 1
        $e["count"] = $events.Count
        $e["id"] = $event.id
        $e["source"] = $event.ProviderName
        try{
            $e_user_sid = new-object System.Security.Principal.SecurityIdentifier(($event.userid).Value)
            $e["user"] = $e_user_sid.translate([System.Security.Principal.NTAccount]).value
        }
        catch{
            $e["user"] = "NA"
        }
        $e["description"] = $event.message
        # $e["logged"] = get-date $event.timecreated -Format o
        $e["machineName"] = $event.machineName
        $id_key = [string]($event.id)
        $out_app_critical[$id_key] = $e
    }
}else{
    $out_app_critical = 0
}
# Finaly dict
$out = @{}
$out["client_version"] = 1
$out["computer"] = $computername
$out["wmi_warning"] = $wmiWarn
$out["system_warnings"] = $out_sys_warning
$out["system_errors"] = $out_sys_error
$out["system_criticals"] = $out_sys_critical
$out["app_warning"] = $out_app_warning
$out["app_errors"] = $out_app_error
$out["app_critical"] = $out_app_critical

try{
    $out | ConvertTo-Json | Out-File $outFile -Encoding utf8 -Force
    return "writeYes"
}catch{
    return 'writeNow'
}