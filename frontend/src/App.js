import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Menu from './pages/Menu';
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/menu" element={<Menu />} />
      </Routes>
    </Router>
  );
}

export default App;
