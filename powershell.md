---
tags: [powershell, guide, api, patterns]
---
<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Master PowerShell Cheat Sheet \& Productivity Guide

PowerShell is Microsoft’s cross-platform command-line shell and automation framework. This guide distills the commands, patterns, and configuration techniques you need to be hyper-productive from any Windows terminal, whether you run Windows PowerShell 5.1 or modern PowerShell 7+.

## Quick-Start Essentials

### Launch \& Help

```powershell
# Current version and edition
$PSVersionTable

# Open PowerShell 7 without loading profiles
pwsh -NoProfile

# Discover cmdlets, aliases, & functions
Get-Command
Get-Command -Noun *Process*

# Search built-in help, then update it
Get-Help Get-Process -Online
Update-Help                     # Admin
```

### Fundamental Operators

| Purpose    | Example                     | Result                      |
|:---------- |:--------------------------- |:--------------------------- |
| Pipeline   | `Get-Process                | Sort-Object CPU -Desc`      |
| Comparison | `$a -ge 10`                 | Greater-or-equal test       |
| Splatting  | `Invoke-RestMethod @Params` | Expands `@Params` hashtable |

## Profiles \& Environment Customization

### Where Are Profiles Stored?

| Scope                                            | Host    | PowerShell 7 Path                                                        | Win PS 5.1 Path                                                          | Runs Automatically |
|:------------------------------------------------ |:------- |:------------------------------------------------------------------------ |:------------------------------------------------------------------------ |:------------------ |
| All Users + All Hosts                            | Console | `$PSHOME\Profile.ps1`[^1]                                                | `$PSHOME\Profile.ps1`[^2]                                                | Yes                |
| All Users + Current Host                         | VS Code | `$PSHOME\Microsoft.VSCode_profile.ps1`[^1]                               | `$PSHOME\Microsoft.PowerShell_profile.ps1`[^2]                           | Yes                |
| Current User + All Hosts                         | Any     | `$HOME\Documents\PowerShell\Profile.ps1`[^1] | `$HOME\Documents\WindowsPowerShell\Profile.ps1`[^3]                      | Yes                |
| Current User + Current Host (default `$PROFILE`) | Console | `$HOME\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`[^4]        | `$HOME\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1`[^5] | Yes                |

### Creating \& Editing

```powershell
# Test existence, then create if missing
if (-not (Test-Path $PROFILE)) { New-Item -ItemType File -Path $PROFILE -Force }

# Open in VS Code
code $PROFILE
```

### Handy Profile Snippets

```powershell
# Colorful prompt showing admin state
function Prompt {
    $admin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(544)
    "$([bool]$admin ? '[ADMIN] ' : '')PS $PWD > "
}

# Import frequently-used modules
Import-Module posh-git
Import-Module oh-my-posh
```

## Core Object Cmdlets

| Action            | Cmdlet           | Example                       |
|:----------------- |:---------------- |:----------------------------- |
| Select properties | `Select-Object`  | `Get-Service                  |
| Filter objects    | `Where-Object`   | `Get-Process                  |
| Sort              | `Sort-Object`    | `Sort-Object StartTime`       |
| Group             | `Group-Object`   | `Get-WinEvent -LogName System |
| Measure           | `Measure-Object` | `Get-ChildItem                |

## Module \& Package Management (PowerShellGet v2)

### Install / Update / Uninstall

```powershell
Install-Module Pester          # Current stable[^21]
Install-Module PSReadLine -Force -AllowPrerelease
Update-Module Pester           # Fetch newest[^34]
Uninstall-Module Pester        # Remove all versions[^23]
```

### PSResourceGet v3 Transition

PowerShell 7.4+ ships *Microsoft.PowerShell.PSResourceGet* alongside PowerShellGet 2.2.5 so you can test faster `*-PSResource` commands without breaking old scripts[^7].

```powershell
Install-PSResource Pester -Scope CurrentUser
Update-PSResource
```

## Script Execution \& Security

| Task                 | Command                                                | Notes                    |
|:-------------------- |:------------------------------------------------------ |:------------------------ |
| Read current policy  | `Get-ExecutionPolicy -List`                            | Machine vs User          |
| Allow local scripts  | `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`  | Needs admin for AllUsers |
| Bypass just this run | `powershell -ExecutionPolicy Bypass -File .\build.ps1` | CI/CD friendly           |

## Running, Debugging \& Testing

### Execute \& Time

```powershell
# Standard run
.\deploy.ps1 -Verbose

# Measure performance
Measure-Command { .\deploy.ps1 }   # Returns a TimeSpan[^41]
```

### Interactive Debugging

| Technique           | Cmdlet/Switch              | Outcome                  |
|:------------------- |:-------------------------- |:------------------------ |
| Command tracing     | `Set-PSDebug -Trace 1`[^8] | Prints each line         |
| Variable strictness | `Set-PSDebug -Strict`[^9]  | Error on unassigned vars |
| Step mode           | `Set-PSDebug -Step`        | Prompt each line         |

### VS Code Integration

1. Install *PowerShell* extension.
2. Press F5 to launch debugger with breakpoints, locals and call-stack.

### Pester Unit Tests

```powershell
Install-Module Pester -Force
Invoke-Pester                      # Runs *.Tests.ps1 files
```

## Performance \& Profiling

| Tool                               | Use-Case                | How-To                                                                                     |
|:---------------------------------- |:----------------------- |:------------------------------------------------------------------------------------------ |
| Measure-Command                    | Quick wall-clock check  | `Measure-Command { Get-ADUser -Filter * }`[^10]                                            |
| Get-Counter                        | Live system metrics     | `Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 2 -MaxSamples 100`[^11] |
| Profiler module                    | Line-level hot spots    | `Install-Module Profiler; Trace-Script script.ps1`[^12]                                    |
| Windows Performance Recorder (ETW) | Deep .NET \& GC insight | `wpr -start PowerShell.wprp -filemode; ...; wpr -stop trace.etl`[^13]                      |

## Filesystem \& Registry Providers

```powershell
# Files
Get-ChildItem -Recurse -Filter *.log | Remove-Item -Force

# Registry
Set-Location HKCU:\Software
Get-ItemProperty .  # Reads current key
```

## Services, Processes \& Jobs

| Action         | Cmdlet                                           |
|:-------------- |:------------------------------------------------ |
| List processes | `Get-Process`                                    |
| Kill process   | `Stop-Process -Id 4242 -Force`                   |
| Background job | `Start-Job -ScriptBlock { Get-EventLog System }` |
| Poll job       | `Receive-Job -Id 3 -Wait -AutoRemoveJob`         |
| Manage service | `Restart-Service spooler`                        |

## Networking \& Web Calls

```powershell
# Quick REST
Invoke-RestMethod https://api.github.com/repos/PowerShell/PowerShell

# Test port
Test-NetConnection www.microsoft.com -Port 443
```

## PowerShell Remoting

| Cmdlet             | Example                                                          |
|:------------------ |:---------------------------------------------------------------- |
| Enable WinRM       | `Enable-PSRemoting -Force`                                       |
| One-off command    | `Invoke-Command -ComputerName SRV01 -ScriptBlock { Get-Uptime }` |
| Persistent session | `$s = New-PSSession SRV01; Enter-PSSession $s`                   |
| SSH transport      | `Enter-PSSession -HostName linux.box -User user1`                |

## Error Handling Patterns

```powershell
try {
    $resp = Invoke-RestMethod $uri -ErrorAction Stop
}
catch [System.Net.WebException] {
    Write-Warning "Network issue: $_"
}
finally {
    'Cleanup done'
}
```

## Formatting \& Output

| Goal            | Cmdlet                                     |
|:--------------- |:------------------------------------------ |
| Table (default) | `Format-Table`                             |
| List            | `Format-List *`                            |
| CSV             | `Export-Csv report.csv -NoTypeInformation` |
| JSON            | `ConvertTo-Json -Depth 4`                  |

## Git Integration Snippets

```powershell
# Show branch in prompt via posh-git
Install-Module posh-git -Scope CurrentUser
Import-Module posh-git
```

## Productivity Aliases (add to profile)

```powershell
Set-Alias ll Get-ChildItem
function gcm { Get-Command -Name $args }
```

## Useful Community Modules

| Module     | Purpose                        | Install                                            |
|:---------- |:------------------------------ |:-------------------------------------------------- |
| PSReadLine | Enhanced editing \& prediction | `Install-Module PSReadLine -Force`                 |
| Az         | Manage Azure                   | `Install-Module Az -Scope CurrentUser -Force`[^14] |
| Pester     | Testing                        | `Install-Module Pester`                            |
| oh-my-posh | Prompt themes                  | `Install-Module oh-my-posh -Scope CurrentUser`     |

## Advanced Topics

### Parallel Execution

```powershell
# ForEach-Object -Parallel (PowerShell 7+)
1..100 | ForEach-Object -Parallel {
    "$_ : $(Get-Date -Format o)"
} -ThrottleLimit 10
```

### Classes \& DSC

PowerShell supports lightweight C\#-style classes for domain models and Desired State Configuration resources.

### Writing Native Modules

Author binary cmdlets with C\# and export them via a `.psd1` manifest.

## PowerShell vs Bash Comparison

| Capability                | PowerShell            | Bash         |
|:------------------------- |:--------------------- |:------------ |
| Object pipe               | Native objects, typed | Byte streams |
| Cross-platform            | Windows, Linux, macOS | Linux first  |
| Verb-Noun discoverability | `Get-Command`         | Varies       |
| Remoting                  | WinRM, SSH            | SSH          |

## Cheat-Sheet Tables

### Frequently-Used Cmdlets

| Category   | Cmdlet          | Mnemonic |
|:---------- |:--------------- |:-------- |
| Discovery  | `Get-Command`   | *gcm*    |
| Inspection | `Get-Member`    | *gm*     |
| Files      | `Get-ChildItem` | *gci*    |
| Text       | `Select-String` | *sls*    |
| Export     | `Export-Csv`    | *ecsv*   |

### Execution Policy Values

| Value        | Meaning                                               |
|:------------ |:----------------------------------------------------- |
| Restricted   | No scripts run                                        |
| RemoteSigned | Local scripts unrestricted, downloaded need signature |
| Bypass       | Nothing blocked                                       |

## One-Day Setup Checklist

1. Install PowerShell 7 from winget or MS Store.
2. `Install-Module PSReadLine, posh-git, oh-my-posh -Scope CurrentUser`.
3. Create `$PROFILE` and paste prompt, aliases, module imports.
4. Set execution policy: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`.
5. Enable PSReadLine predictors:

```powershell
Set-PSReadLineOption -PredictionSource HistoryAndPlugin
```

## Performance Tuning Tips

- Use provider-specific `-Filter` instead of piping large sets[^10].
- Avoid repeatedly calling external EXE inside loops; capture once.
- Profile code paths with *Profiler* module and focus on high self-time nodes[^12].

## Troubleshooting Flow

1. Run with `-Verbose` / `-Debug` streams.
2. Trace lines via `Set-PSDebug -Trace 2`[^8].
3. Use `Write-Debug` inside functions for conditional output.
4. Step through in VS Code debugger.

## Appendix A: Regular Expression Cheats

| Pattern          | Goal                 |
|:---------------- |:-------------------- |
| `\d+`            | One or many digits   |
| `^\s*$`          | Empty line           |
| `(?<=prefix)\w+` | Positive look-behind |

## Appendix B: Special Variables

| Variable | Meaning                 |
|:-------- |:----------------------- |
| `$?`     | Success of last command |
| `$_`     | Current pipeline item   |
| `$PID`   | Current process ID      |
| `$$`     | Last token of last line |

## Appendix C: Numeric Format Strings

| Format   | Example  |
|:-------- |:-------- |
| `{0:N2}` | 1,234.57 |
| `{0:P1}` | 12.3%    |

PowerShell’s object pipeline, rich module ecosystem, and tight integration with .NET make it a powerhouse for automation and interactive work alike. Keep this cheat-sheet handy, customize your profile, and embrace modules and profiling tools to unlock maximum productivity.

<div style="text-align: center">⁂</div>

[^1]: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles?view=powershell-7.5

[^2]: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles?view=powershell-7.4\&viewFallbackFrom=powershell-7.3

[^3]: https://forums.powershell.org/t/powershell-profile-location/6329

[^4]: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles?view=powershell-7.5\&rut=ca2f8dc01488630fbee78df9e4216fa25624c191e87663f49656f078181e1f83

[^5]: https://renenyffenegger.ch/notes/Windows/PowerShell/language/variable/automatic/profile

[^6]: https://powershellisfun.com/2024/06/14/using-measure-command-and-measure-object-in-powershell/

[^7]: https://devblogs.microsoft.com/powershell/powershellget-in-powershell-7-4-updates/

[^8]: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/set-psdebug?view=powershell-7.5

[^9]: https://devblogs.microsoft.com/scripting/troubleshoot-by-using-set-psdebug/

[^10]: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/measure-command?view=powershell-7.5

[^11]: https://learn.microsoft.com/en-us/previous-versions/technet-magazine/ee872428(v=msdn.10)?redirectedfrom=MSDN

[^12]: https://powershellisfun.com/2024/02/01/using-the-powershell-profiler-module/

[^13]: https://fossies.org/linux/PowerShell/tools/performance/README.md

[^14]: https://learn.microsoft.com/en-us/powershell/azure/install-azps-windows?view=azps-12.5.0\&viewFallbackFrom=azps-13.5.0

[^15]: https://www.techtarget.com/searchwindowsserver/tutorial/How-to-find-and-customize-your-PowerShell-profile

[^16]: https://www.microsoft.com/en-us/dynamics-365/blog/business-leader/2015/03/10/coffee-break-creating-and-using-windows-powershell-profiles/

[^17]: https://www.howtogeek.com/126469/how-to-create-a-powershell-profile/

[^18]: https://stackoverflow.com/questions/8997316/powershell-profile-is-pointing-to-a-path-that-i-cant-find-and-setting-permane

[^19]: https://learn.microsoft.com/en-us/powershell/scripting/learn/shell/creating-profiles?view=powershell-7.5

[^20]: https://devblogs.microsoft.com/scripting/powertip-use-powershell-to-find-user-profile-path/

[^21]: https://learn.microsoft.com/en-us/powershell/scripting/learn/shell/creating-profiles?view=powershell-7.5\&rut=dcaf48a9e78c63230626c593d4d3a427557a9a65f60a4271a735163722800238

[^22]: https://superuser.com/questions/1830670/what-is-the-currently-the-preferred-location-of-powershell-profiles

[^23]: https://learn.microsoft.com/en-us/powershell/scripting/learn/shell/creating-profiles?view=powershell-7.5\&rut=26a043d4d65e4b04701f3659c4daf38ae9c52d26ddd7e331511b52023bd3db98

[^24]: https://www.techtarget.com/searchitoperations/answer/Manage-the-Windows-PATH-environment-variable-with-PowerShell

[^25]: https://stackoverflow.com/questions/75540911/how-do-i-create-a-profile-in-powershell-7-3-2

[^26]: https://www.reddit.com/r/PowerShell/comments/1gchmsb/is_it_possible_to_change_the_profile_path/

[^27]: https://stackoverflow.com/questions/36239010/how-do-i-recreate-powershell-profile-variable-its-empty-in-a-custom-host

[^28]: https://stackoverflow.com/questions/39809315/windows-powershell-profile-does-not-show-a-real-path

[^29]: https://scottmckendry.tech/the-ultimate-powershell-profile/

[^30]: https://learn.microsoft.com/en-us/powershell/module/powershellget/install-module?view=powershellget-3.x

[^31]: https://www.powershellgallery.com/packages/UpdateInstalledModule/1.1/Content/Update-InstalledModule.ps1

[^32]: https://learn.microsoft.com/en-us/powershell/module/powershellget/uninstall-module?view=powershellget-3.x

[^33]: https://www.devopsschool.com/blog/what-is-powershellget-and-how-to-install-powershellget-3-0/

[^34]: https://www.pdq.com/powershell/update-module/

[^35]: https://www.powershellgallery.com/packages/spec.module.management/1.0.2/Content/Public\Uninstall-specModule.ps1

[^36]: https://blog.idera.com/database-tools/powershell/powertips/test-driving-powershellget-version-3/

[^37]: https://www.comparitech.com/net-admin/install-powershell-modules/

[^38]: https://www.powershellgallery.com/packages/UpdateInstalledModule/1.0/Content/Update-InstalledModule.ps1

[^39]: https://www.pdq.com/powershell/uninstall-module/

[^40]: https://devblogs.microsoft.com/powershell/powershellget-3-0-preview-1/

[^41]: https://www.pdq.com/powershell/install-module/

[^42]: https://learn.microsoft.com/en-us/powershell/module/powershellget/update-module?view=powershellget-3.x

[^43]: https://learn.microsoft.com/th-th/powershell/module/powershellget/uninstall-module?view=powershellget-1.x

[^44]: https://www.powershellgallery.com/packages/PowerShellGet/3.0.22-beta22

[^45]: https://subscription.packtpub.com/book/cloud-and-networking/9781787126305/3/ch03lvl1sec25/the-install-module-command

[^46]: https://powershellisfun.com/2022/07/11/updating-your-powershell-modules-to-the-latest-version-plus-cleaning-up-older-versions/

[^47]: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/remove-module?view=powershell-7.5

[^48]: https://docs.poshtools.com/powershell-pro-tools-documentation/visual-studio-code/profiler

[^49]: https://www.pdq.com/powershell/measure-command/

[^50]: https://www.pdq.com/powershell/set-psdebug/

[^51]: https://stackoverflow.com/questions/78087292/how-to-use-measure-command-in-a-powershell-script

[^52]: https://devblogs.microsoft.com/scripting/powertip-use-powershell-to-find-performance-of-processes/

[^53]: https://subscription.packtpub.com/book/cloud-and-networking/9781782173571/7/ch07lvl1sec53/using-set-psdebug

[^54]: https://docs.powershelluniversal.com/v4-beta/development/profiling

[^55]: https://www.youtube.com/watch?v=nG4gkXTIa-s

[^56]: https://devblogs.microsoft.com/premier-developer/powershell-profiling/

[^57]: https://blog.ironmansoftware.com/runtime-diagnostics/

[^58]: https://fossies.org/dox/PowerShell-7.4.5/md_tools_2performance_2README.html

[^59]: https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/set-psdebug?view=powershell-7.4\&viewFallbackFrom=powershell-7

[^60]: https://theniceweb.com/archives/471

## Related Concepts

### Related Topics
- [[dotnet]] - PowerShell often used alongside .NET development
- [[cpp_project]] - PowerShell used for C++ build automation on Windows
- [[windows_app_sdk_setup]] - PowerShell used for Windows environment configuration
- [[cli]] - Similar CLI patterns in different languages
- [[cargo]] - Cargo used from PowerShell command line on Windows

### Extended By
- [[cpp_project]] - PowerShell used for Windows environment and build automation
- [[windows_app_sdk_setup]] - PowerShell used for Windows environment configuration

### Alternatives
- [[cli]] - Rust CLI alternative for cross-platform tools