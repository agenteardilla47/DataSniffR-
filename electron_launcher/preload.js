const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('sigil', {
  scan: (text) => ipcRenderer.invoke('scan-text', text)
});