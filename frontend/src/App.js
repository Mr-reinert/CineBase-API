// frontend/src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import MovieDetailPage from './pages/MovieDetailPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import { useAuth } from './contexts/AuthContext';

function App() {
    const { user, logout } = useAuth();

    return (
        <Router>
            <nav style={{ padding: '10px', background: '#f0f0f0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <Link to="/" style={{ marginRight: '15px' }}>Início</Link>
                    {user ? (
                        <>
                            <Link to="/profile" style={{ marginRight: '15px' }}>Meu Perfil</Link>
                            <button onClick={logout} style={{ border: 'none', background: 'none', cursor: 'pointer', color: 'blue' }}>Sair</button>
                        </>
                    ) : (
                        <>
                            <Link to="/login" style={{ marginRight: '15px' }}>Login</Link>
                            <Link to="/register">Registrar</Link>
                        </>
                    )}
                </div>
                {user && <span>Bem-vindo, {user.name}!</span>}
            </nav>

            <div style={{ padding: '20px' }}>
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/filmes/:id" element={<MovieDetailPage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/profile" element={<ProfilePage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;