// frontend/src/contexts/AuthContext.js
import React, { createContext, useState, useEffect, useContext } from 'react';
import api from '../services/api'; // Importa a instância do axios configurada
import { jwtDecode } from 'jwt-decode'; // Para decodificar o token JWT

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    // Efeito para carregar o usuário logado ao iniciar a aplicação
    useEffect(() => {
        const loadUser = async () => {
            const token = localStorage.getItem('accessToken');
            if (token) {
                try {
                    const decodedToken = jwtDecode(token);
                    // Verifica se o token não expirou
                    if (decodedToken.exp * 1000 < Date.now()) {
                        localStorage.removeItem('accessToken');
                        setUser(null);
                    } else {
                        // Se o token existe e é válido, busca os dados do usuário
                        const response = await api.get('/usuarios/me');
                        setUser(response.data);
                    }
                } catch (error) {
                    console.error('Erro ao decodificar ou buscar usuário:', error);
                    localStorage.removeItem('accessToken');
                    setUser(null);
                }
            }
            setLoading(false);
        };
        loadUser();
    }, []);

    const login = async (email, password) => {
        try {
            // Requisição POST para o endpoint de login do backend
            const response = await api.post('/login/', { username: email, password: password });
            const { access_token } = response.data;
            localStorage.setItem('accessToken', access_token); // Armazena o token

            // Após login, busca os dados do usuário atual para popular o estado
            const userResponse = await api.get('/usuarios/me');
            setUser(userResponse.data);
            return true;
        } catch (error) {
            console.error('Erro no login:', error.response?.data?.detail || error.message);
            throw error; // Re-lança o erro para o componente lidar
        }
    };

    const register = async (name, email, password) => {
        try {
            // Requisição POST para o endpoint de registro do backend
            const response = await api.post('/usuarios/', { name, email, password });
            console.log('Usuário registrado com sucesso:', response.data);
            return true;
        } catch (error) {
            console.error('Erro no registro:', error.response?.data?.detail || error.message);
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem('accessToken'); // Remove o token
        setUser(null); // Limpa o estado do usuário
    };

    return (
        <AuthContext.Provider value={{ user, loading, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);