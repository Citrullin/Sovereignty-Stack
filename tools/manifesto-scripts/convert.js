const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { program } = require('commander');
const puppeteer = require('puppeteer');
const MarkdownIt = require('markdown-it');
const mk = require('markdown-it-katex');

const katexCssPath = path.resolve('node_modules/katex/dist/katex.min.css');
const katexCss = fs.existsSync(katexCssPath) ? fs.readFileSync(katexCssPath, 'utf8') : '';

program
  .name('eth-md-converter')
  .description('Convert Markdown with LaTeX and diagrams to PDF and SVGs')
  .argument('<file>', 'Markdown file to process')
  .option('-o, --output <type>', 'Output base filename', 'output')
  .option('--no-pdf', 'Disable PDF generation')
  .action(main);

program.parse();

async function processDiagrams(markdown, assetsDir) {
  const regex = /```(graphviz|yuml|plantuml|mermaid)\n([\s\S]*?)```/g;
  let processedMd = markdown;
  let m;

  // We need to loop manually because we might have async calls
  const matches = [...markdown.matchAll(regex)];

  for (const match of matches) {
    const fullBlock = match[0];
    const type = match[1];
    const source = match[2].trim();

    // Generate hash for filename
    const hash = crypto.createHash('md5').update(`type:${type}:source:${source}`).digest('hex');
    const filename = `${type}_${hash.substring(0, 8)}.svg`;
    const filepath = path.join(assetsDir, filename);

    if (!fs.existsSync(filepath)) {
      console.log(`Generating SVG for ${type} diagram...`);
      try {
        const response = await fetch(`https://kroki.io/${type}/svg`, {
          method: 'POST',
          headers: {
            'Content-Type': 'text/plain',
          },
          body: source
        });
        
        if (!response.ok) {
          throw new Error(`Kroki responded with ${response.status}: ${await response.text()}`);
        }

        const svgContent = await response.text();
        fs.writeFileSync(filepath, svgContent);
        console.log(`Saved diagram to ${filepath}`);
      } catch (err) {
        console.error(`Failed to generate diagram for ${type}:`, err);
        continue;
      }
    }

    // Replace the specific block in the markdown
    const mdImg = `![${type} diagram](${path.join(path.basename(assetsDir), filename).replace(/\\/g, '/')})`;
    processedMd = processedMd.replace(fullBlock, mdImg);
  }

  return processedMd;
}

async function main(inputFile, options) {
  if (!fs.existsSync(inputFile)) {
    console.error(`File not found: ${inputFile}`);
    process.exit(1);
  }

  const baseName = options.output || path.basename(inputFile, path.extname(inputFile));
  const assetsDir = path.join(path.dirname(inputFile), `${baseName}_assets`);
  
  if (!fs.existsSync(assetsDir)) {
    fs.mkdirSync(assetsDir, { recursive: true });
  }

  const rawMd = fs.readFileSync(inputFile, 'utf-8');

  console.log('Processing diagrams...');
  const processedMd = await processDiagrams(rawMd, assetsDir);

  // Write the preprocessed markdown out for Ethresearch usage
  const processedMdPath = `${baseName}_clean.md`;
  fs.writeFileSync(processedMdPath, processedMd);
  console.log(`Saved preprocessed Markdown to ${processedMdPath} (Great for Ethresearch posts!)`);

  if (options.pdf === false) {
    return;
  }

  console.log('Rendering Markdown to HTML...');
  const md = new MarkdownIt({ html: true });
  md.use(mk); // adds katex support

  const renderedHtml = md.render(processedMd);

  let htmlDoc = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>/* KATEX_CSS_INJECT */</style>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
      line-height: 1.6;
      color: #333;
      max-width: 800px;
      margin: 0 auto;
      padding: 2cm;
      background: white;
    }
    .katex .frac-line { border-bottom-width: 1px !important; transform: scaleY(0.5); }
    .katex {
      text-rendering: optimizeLegibility;
      -webkit-font-smoothing: antialiased;
    }
    @media print {
      body {
        max-width: none;
        margin: 0;
        padding: 0;
      }
      .page-break { page-break-before: always; }
    }
    pre { background: #f6f8fa; padding: 16px; border-radius: 6px; overflow: auto; page-break-inside: avoid; }
    code { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; background: #f6f8fa; padding: .2em .4em; border-radius: 6px;}
    pre code { background: none; padding: 0; }
    h1, h2, h3, h4, h5, h6 { border-bottom: 1px solid #eee; padding-bottom: 0.3em; margin-top: 1.5em; page-break-after: avoid; }
    h1 { font-size: 24pt; }
    h2 { font-size: 18pt; }
    h3 { font-size: 14pt; }
    blockquote { border-left: 4px solid #dfe2e5; padding: 0 1em; color: #6a737d; margin-left: 0; }
    img { width: 100%; height: auto; display: block; margin: 1em 0; }
  </style>
</head>
<body>
  <!-- Hidden font primer to force-load KaTeX glyphs before PDF capture -->
  <div style="visibility: hidden; position: absolute; top: 0; left: 0;">
    ${String.raw`$\sum \int \alpha \beta \gamma \delta \epsilon \zeta \eta \theta \iota \kappa \lambda \mu \nu \xi \omicron \pi \rho \sigma \tau \upsilon \phi \chi \psi \omega$`}
  </div>
  ${renderedHtml}
</body>
</html>
  `;

  htmlDoc = htmlDoc.replace('/* KATEX_CSS_INJECT */', katexCss);

  const htmlPath = `${baseName}.html`;
  fs.writeFileSync(htmlPath, htmlDoc);
  console.log(`Saved HTML to ${htmlPath}`);

  console.log('Generating PDF with Puppeteer...');
  const browser = await puppeteer.launch({
    args: ['--disable-web-security']
  });
  const page = await browser.newPage();
  
  // Resolve absolute path for local files to load correctly in puppeteer
  const fileUrl = 'file://' + path.resolve(htmlPath);
  await page.goto(fileUrl, { waitUntil: 'networkidle0' });

  // Explicitly wait for fonts to be ready to prevent disjointed summation/integral symbols
  await page.evaluateHandle('document.fonts.ready');
  // Addition safety buffer for complex layout math to settle
  await new Promise(r => setTimeout(r, 600));

  const pdfPath = `${baseName}.pdf`;
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    margin: { top: '2cm', right: '2cm', bottom: '2cm', left: '2cm' },
    printBackground: true
  });

  await browser.close();
  console.log(`Successfully generated PDF: ${pdfPath}`);
}
