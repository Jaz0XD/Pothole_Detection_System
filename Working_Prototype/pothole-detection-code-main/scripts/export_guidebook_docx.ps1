param(
    [string]$InputPath = "docs/developer_guidebook.md",
    [string]$OutputPath = "docs/Pothole_Detection_Prototype_Guidebook.docx"
)

$ErrorActionPreference = "Stop"

function Escape-XmlText {
    param([string]$Text)
    if ($null -eq $Text) { return "" }
    $escaped = $Text.Replace("&", "&amp;").Replace("<", "&lt;").Replace(">", "&gt;")
    return $escaped
}

function Convert-MarkdownToPlainText {
    param([string]$Text)
    if ($null -eq $Text) { return "" }

    $clean = $Text
    $clean = $clean -replace '\[([^\]]+)\]\([^)]+\)', '$1'
    $clean = $clean -replace '`([^`]*)`', '$1'
    $clean = $clean -replace '\*\*([^*]+)\*\*', '$1'
    $clean = $clean -replace '\*([^*]+)\*', '$1'
    $clean = $clean -replace '^>\s*', ''
    return $clean.TrimEnd()
}

function New-ParagraphXml {
    param(
        [string]$Text,
        [string]$Style = "Normal"
    )

    $plainText = Convert-MarkdownToPlainText $Text
    $xmlSafe = Escape-XmlText $plainText
    return "<w:p><w:pPr><w:pStyle w:val=`"$Style`"/></w:pPr><w:r><w:t xml:space=`"preserve`">$xmlSafe</w:t></w:r></w:p>"
}

function New-DocxPackage {
    param(
        [string]$MarkdownPath,
        [string]$DocxPath
    )

    if (-not (Test-Path -LiteralPath $MarkdownPath)) {
        throw "Input file not found: $MarkdownPath"
    }

    $lines = Get-Content -LiteralPath $MarkdownPath
    $bodyParts = New-Object System.Collections.Generic.List[string]
    $inCodeBlock = $false
    $isFirstTitle = $true

    foreach ($line in $lines) {
        if ($line -match '^```') {
            $inCodeBlock = -not $inCodeBlock
            continue
        }

        if ($inCodeBlock) {
            $bodyParts.Add((New-ParagraphXml -Text $line -Style "CodeBlock"))
            continue
        }

        if ([string]::IsNullOrWhiteSpace($line)) {
            continue
        }

        if ($line.StartsWith("# ")) {
            $style = if ($isFirstTitle) { "Title" } else { "Heading1" }
            $isFirstTitle = $false
            $bodyParts.Add((New-ParagraphXml -Text $line.Substring(2) -Style $style))
            continue
        }

        if ($line.StartsWith("## ")) {
            $bodyParts.Add((New-ParagraphXml -Text $line.Substring(3) -Style "Heading1"))
            continue
        }

        if ($line.StartsWith("### ")) {
            $bodyParts.Add((New-ParagraphXml -Text $line.Substring(4) -Style "Heading2"))
            continue
        }

        if ($line -match '^- ') {
            $bodyParts.Add((New-ParagraphXml -Text ("- " + $line.Substring(2)) -Style "ListParagraph"))
            continue
        }

        if ($line -match '^\d+\.\s') {
            $bodyParts.Add((New-ParagraphXml -Text $line -Style "ListParagraph"))
            continue
        }

        $bodyParts.Add((New-ParagraphXml -Text $line -Style "Normal"))
    }

    $bodyParts.Add('<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1440" w:right="1080" w:bottom="1440" w:left="1080" w:header="708" w:footer="708" w:gutter="0"/></w:sectPr>')
    $documentBody = ($bodyParts -join "")

    $contentTypes = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>
'@

    $rels = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
'@

    $documentXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"
 xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
 xmlns:o="urn:schemas-microsoft-com:office:office"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"
 xmlns:v="urn:schemas-microsoft-com:vml"
 xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
 xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
 xmlns:w10="urn:schemas-microsoft-com:office:word"
 xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
 xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"
 xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup"
 xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk"
 xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml"
 xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape"
 mc:Ignorable="w14 wp14">
  <w:body>$documentBody</w:body>
</w:document>
"@

    $stylesXml = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:sz w:val="24"/>
      </w:rPr>
    </w:rPrDefault>
    <w:pPrDefault>
      <w:pPr>
        <w:jc w:val="both"/>
      </w:pPr>
    </w:pPrDefault>
  </w:docDefaults>
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:pPr>
      <w:jc w:val="both"/>
      <w:spacing w:after="120" w:line="360" w:lineRule="auto"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="24"/>
    </w:rPr>
    <w:qFormat/>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Title">
    <w:name w:val="Title"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:jc w:val="center"/>
      <w:spacing w:before="240" w:after="240"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="34"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:jc w:val="left"/>
      <w:spacing w:before="240" w:after="120"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="28"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:next w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:jc w:val="left"/>
      <w:spacing w:before="180" w:after="80"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="ListParagraph">
    <w:name w:val="List Paragraph"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:ind w:left="720" w:hanging="360"/>
      <w:spacing w:after="40"/>
      <w:jc w:val="both"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="24"/>
    </w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="CodeBlock">
    <w:name w:val="CodeBlock"/>
    <w:basedOn w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:ind w:left="360" w:right="360"/>
      <w:spacing w:before="20" w:after="20"/>
      <w:shd w:val="clear" w:color="auto" w:fill="F3F6FA"/>
      <w:jc w:val="left"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="20"/>
    </w:rPr>
  </w:style>
</w:styles>
'@

    $timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    $coreXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/"
 xmlns:dcterms="http://purl.org/dc/terms/"
 xmlns:dcmitype="http://purl.org/dc/dcmitype/"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>Pothole Detection Prototype Guidebook</dc:title>
  <dc:subject>Developer Guidebook and User Manual</dc:subject>
  <dc:creator>OpenAI Codex</dc:creator>
  <cp:keywords>pothole detection, developer guide, user manual, RC car, ESP32</cp:keywords>
  <dc:description>Report-style guidebook generated from the repository documentation.</dc:description>
  <cp:lastModifiedBy>OpenAI Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">$timestamp</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">$timestamp</dcterms:modified>
</cp:coreProperties>
"@

    $appXml = @'
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"
 xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft Office Word</Application>
  <DocSecurity>0</DocSecurity>
  <ScaleCrop>false</ScaleCrop>
  <Company></Company>
  <LinksUpToDate>false</LinksUpToDate>
  <SharedDoc>false</SharedDoc>
  <HyperlinksChanged>false</HyperlinksChanged>
  <AppVersion>16.0000</AppVersion>
</Properties>
'@

    $tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("guidebook_docx_" + [guid]::NewGuid().ToString("N"))
    $null = New-Item -ItemType Directory -Path $tempRoot
    $null = New-Item -ItemType Directory -Path (Join-Path $tempRoot "_rels")
    $null = New-Item -ItemType Directory -Path (Join-Path $tempRoot "docProps")
    $null = New-Item -ItemType Directory -Path (Join-Path $tempRoot "word")

    Set-Content -LiteralPath (Join-Path $tempRoot "[Content_Types].xml") -Value $contentTypes -Encoding UTF8
    Set-Content -LiteralPath (Join-Path $tempRoot "_rels\.rels") -Value $rels -Encoding UTF8
    Set-Content -LiteralPath (Join-Path $tempRoot "word\document.xml") -Value $documentXml -Encoding UTF8
    Set-Content -LiteralPath (Join-Path $tempRoot "word\styles.xml") -Value $stylesXml -Encoding UTF8
    Set-Content -LiteralPath (Join-Path $tempRoot "docProps\core.xml") -Value $coreXml -Encoding UTF8
    Set-Content -LiteralPath (Join-Path $tempRoot "docProps\app.xml") -Value $appXml -Encoding UTF8

    $zipPath = [System.IO.Path]::ChangeExtension($DocxPath, ".zip")
    $outputDir = Split-Path -Parent $DocxPath
    if (-not [string]::IsNullOrWhiteSpace($outputDir)) {
        $null = New-Item -ItemType Directory -Force -Path $outputDir
    }

    if (Test-Path -LiteralPath $zipPath) {
        Remove-Item -LiteralPath $zipPath -Force
    }
    if (Test-Path -LiteralPath $DocxPath) {
        Remove-Item -LiteralPath $DocxPath -Force
    }

    Compress-Archive -Path (Join-Path $tempRoot "*") -DestinationPath $zipPath -Force
    Move-Item -LiteralPath $zipPath -Destination $DocxPath -Force
    Remove-Item -LiteralPath $tempRoot -Recurse -Force
}

New-DocxPackage -MarkdownPath $InputPath -DocxPath $OutputPath
Write-Host "Generated $OutputPath"
