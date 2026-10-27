$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open("D:\Vibe code\BTL_DACN_CNPM\BTL_DACN_CNPM.docx")
    foreach ($p in $doc.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^Hình\s+4\.\d+") {
            $page = $p.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndPageNumber)
            Write-Host "$txt ===> Page $page"
        }
    }
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
}
