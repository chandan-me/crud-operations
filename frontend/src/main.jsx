/**
 * main.jsx
 * --------
 * The JavaScript entry point of the React frontend application.
 
 * It uses ReactDOM.createRoot to mount the root App component into the HTML document's <div id="root"> element.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './App.css';

// Mount the App component inside the #root DOM element
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

