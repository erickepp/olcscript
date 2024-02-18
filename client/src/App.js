import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import Index from './pages/Index';
import Errors from './pages/Errors';
import SymbolTable from './pages/SymbolTable';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/errors" element={<Errors />} />
        <Route path="/symbol-table" element={<SymbolTable />} />
        <Route path="*" element={<Navigate to="/" replace={true} />} exact={true} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
