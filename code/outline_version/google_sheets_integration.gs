
//EL CÓDIGO VA PEGADO EN UN SCRIPT DE GOOGLE SHEETS
//RECORDAR PEGAR EL LINK DE LA HOJA DE GOOGLE AL CREAR EL WEBHOOK PARA ESTRABLECER LA COMUNICACIÓN ENTRE OUTLINE Y LA HOJA DE GOOGLE

function doPost(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('NOMBRE_DE_LA_HOJA');
  const data = JSON.parse(e.postData.contents);

  const timestamp = new Date();
  const event = data.event || 'unknown';
  const docId = data.payload?.id || '';
  const title = data.payload?.model?.title || '';
  const actorId = data.actorId || '';
  const actorName = data.payload?.model?.updatedBy?.name || '';

  sheet.appendRow([timestamp, event, docId, title, actorId, actorName]);

  // Always return a 200 OK quickly
  return ContentService.createTextOutput('OK');
}