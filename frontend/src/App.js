import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Menu from './pages/Menu';
import First from './pages/First';
import Second from './pages/Second'
import Receipt from './pages/Receipt'
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<First />} />
        <Route path="/menu" element={<Menu />} />
        <Route path="/Second" element={<Second />} />
        <Route path="/Receipt" element={<Receipt />} />
      </Routes>
    </Router>
  );
}

export default App;
