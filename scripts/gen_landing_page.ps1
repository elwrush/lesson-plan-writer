param([string]$Workdir)

Push-Location $Workdir

$allPresentations = @()
git ls-tree --name-only HEAD | Where-Object { $_ -ne "index.html" } | ForEach-Object {
    $dir = $_
    $htmlPath = "$dir/index.html"
    $title = "Presentation"
    if (Test-Path $htmlPath) {
        $content = Get-Content $htmlPath -Raw
        if ($content -match '<title>(.*?)</title>') {
            $title = $matches[1]
        }
    }
    $allPresentations += @{ dir = $dir; title = $title }
}

$cardsHtml = ""
foreach ($p in $allPresentations) {
    $cardsHtml += @"
            <a href="$($p.dir)/" class="card">
                <div class="card-title">$($p.title)</div>
                <div class="card-dir">$($p.dir)</div>
            </a>

"@
}

$landingPage = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Lesson Plan Slides</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #f0f2f5;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 60px 20px;
        }
        h1 {
            font-size: 2.2em;
            color: #1a1a2e;
            margin-bottom: 40px;
            text-align: center;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            max-width: 960px;
            width: 100%;
        }
        .card {
            background: white;
            border-radius: 12px;
            padding: 28px 24px;
            text-decoration: none;
            color: #333;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            transition: transform 0.2s, box-shadow 0.2s;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        }
        .card-title {
            font-size: 1.15em;
            font-weight: 600;
            color: #1a1a2e;
        }
        .card-dir {
            font-size: 0.85em;
            color: #888;
            font-family: 'Consolas', monospace;
        }
        footer {
            margin-top: 50px;
            font-size: 0.85em;
            color: #aaa;
        }
    </style>
</head>
<body>
    <h1>Lesson Plan Slides</h1>
    <div class="grid">
$cardsHtml    </div>
    <footer>Lesson Plan Writer 3</footer>
</body>
</html>
"@

Set-Content -Path "index.html" -Value $landingPage -NoNewline
Write-Host "Landing page generated with $($allPresentations.Count) presentation(s)"

Pop-Location
