const { chromium } = require('playwright');
const path = require('path');

const pages = ['', '-download', '-example', '-html', '-layouts', '-paraview', '-setup-vtk'];

const style = `
`;

(async () => {
  const browser = await chromium.launch()
  for (const pageName of pages) {
    const page = await browser.newPage()
    //const filename = `build-tmp/public/docs/tutorial${pageName}.html`
    // await page.goto(`file:${path.join(__dirname, filename)}`)
    const url = `http://kitware.github.io/trame/docs/tutorial${pageName}.html`
    await page.addStyleTag({content: style})
    await page.goto(url)
    await page.pdf({ path: path.join(__dirname, (pageName.replace(/^-/, '') || 'trame') + ".pdf") })
  }
  await browser.close()
})()
