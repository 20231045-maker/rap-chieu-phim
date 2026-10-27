$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open("D:\Vibe code\BTL_DACN_CNPM\BTL_DACN_CNPM.docx")
    foreach ($p in $doc.Paragraphs) {
        $txt = $p.Range.Text.Trim()
        if ($txt -like "CHƯƠNG*" -or $txt -in @("LỜI CẢM ƠN", "LỜI MỞ ĐẦU", "MỤC LỤC", "DANH MỤC HÌNH VẼ", "DANH MỤC BẢNG BIỂU", "KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", "TÀI LIỆU THAM KHẢO")) {
            $page = $p.Range.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndPageNumber)
            Write-Host "$txt -> Page $page"
        }
    }
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
}
