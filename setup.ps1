$root = "C:\Seria Internship\Auto_Dealer\auto_dealer"

$dirs = @(
    "$root",
    "$root\auto_dealer",
    "$root\auto_dealer\doctype",
    "$root\auto_dealer\doctype\vehicle",
    "$root\auto_dealer\doctype\vehicle_sale",
    "$root\auto_dealer\doctype\test_drive",
    "$root\auto_dealer\doctype\service_job_card",
    "$root\auto_dealer\doctype\insurance_policy",
    "$root\auto_dealer\doctype\loan_application",
    "$root\auto_dealer\doctype\oem_target",
    "$root\auto_dealer\report",
    "$root\auto_dealer\print_format",
    "$root\auto_dealer\workflow",
    "$root\api",
    "$root\public"
)

foreach ($d in $dirs) {
    New-Item -ItemType Directory -Path $d -Force | Out-Null
}

$files = @(
    "$root\hooks.py",
    "$root\modules.txt",
    "$root\api\whatsapp.py",
    "$root\api\insurance.py",
    "$root\api\loan_dsa.py",
    "$root\api\marketplace_sync.py"
)

foreach ($f in $files) {
    New-Item -ItemType File -Path $f -Force | Out-Null
}

Write-Host "Done."
