const { chromium } = require('playwright');
const path = require('path');

const pages = ['', '-download', '-example', '-setup-vtk', '-vtk', '-layouts', '-html', '-application', '-paraview'];
// const pages = ['-html']

// const host = "http://kitware.github.io";
const host = "http://localhost:4000";

(async () => {
  const browser = await chromium.launch()
  console.log("Starting pdf generation");
  for (const pageName of pages) {
    const page = await browser.newPage()
    const url = `${host}/trame/docs/tutorial${pageName}.html`
    await page.goto(url)
    await page.pdf({ path: path.join(__dirname, (pageName.replace(/^-/, '') || 'trame') + ".pdf") })
    console.log("Saved ", path.join(__dirname, (pageName.replace(/^-/, '') || 'trame') + ".pdf"))
  }
  await browser.close()
})()
