// Optional future Apps Script sketch. Do not store credentials in this file.
function createStockDocument(title, body) {
  const doc = DocumentApp.create(title);
  doc.getBody().setText(body);
  doc.saveAndClose();
  return doc.getUrl();
}
