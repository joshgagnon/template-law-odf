# template-law-odf
Generate ODF documents from jinja2 templated ODT files


/Applications/LibreOffice.app/Contents/MacOS/soffice "-env:UserInstallation=file:///tmp/LibO_Conversion" --headless --invisible --convert-to pdf --outdir ~/template-law-odf/out out.odt