import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import USB from './components/usb_device_list'

const root = ReactDOM.createRoot(document.getElementById('root'));
const usb_devices = ReactDOM.createRoot(document.getElementById('usb'));

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);


usb_devices.render(
  <React.StrictMode>
    <USB />
  </React.StrictMode>
);
