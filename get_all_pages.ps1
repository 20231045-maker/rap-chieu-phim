$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open("D:\Vibe code\BTL_DACN_CNPM\BTL_DACN_CNPM.docx")
    Write-Host "=== HEADINGS & SECTIONS ==="
    foreach ($p in $doc.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -match "^(CHƯƠNG\s+[IVX]+|\d+\.\d+(\.\d+)?|LỜI CẢM ƠN|LỜI MỞ ĐẦU|MỤC LỤC|DANH MỤC|KẾT LUẬN|TÀI LIỆU|PHỤ LỤC)") {
            $page = $p.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndPageNumber)
            Write-Host "$txt ===> Page $page"
        }
    }
    Write-Host "=== TABLES ==="
    foreach ($t in $doc.Tables) {
        $captionP = $t.Range.Paragraphs.Item(1).Previous()
        if ($captionP) {
            $capText = $captionP.Range.Text.Trim()
            if ($capText -match "^Bảng\s+\d+\.\d+") {
                $page = $captionP.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndPageNumber)
                Write-Host "$capText ===> Page $page"
            }
        }
    }
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
}
