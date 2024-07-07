import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Menu from './pages/Menu';
import First from './pages/First';
import Second from './pages/Second'
import Receipt from './pages/Receipt'
import Description from './pages/Description';
import HowToPay from './pages/HowToPay';
import Pay from './pages/Pay';
import Point from './pages/Point';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<First />} />
        <Route path="/menu" element={<Menu />} />
        <Route path="/wheretoeat" element={<Second />} />
        <Route path='/description' element={<Description />} />
        <Route path="/howtopay" element={<HowToPay />} />
        <Route path="/pay" element={<Pay />} />
        <Route path="/point" element={<Point />} />
        <Route path="/receipt" element={<Receipt />} />
      </Routes>
    </Router>
  );
}

export default App;
