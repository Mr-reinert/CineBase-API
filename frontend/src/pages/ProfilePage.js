// frontend/src/pages/ProfilePage.js
import React from 'react';
import { useAuth } from '../contexts/AuthContext'; // Importa o hook useAuth
import { Navigate } from 'react-router-dom'; // Para redirecionar se não estiver logado

function ProfilePage() {
    const { user, loading } = useAuth(); // Obtém o usuário e o estado de carregamento do contexto

    // Exibe mensagem de carregamento enquanto o estado do usuário está sendo verificado
    if (loading) {
        return <p>Carregando perfil...</p>;
    }

    // Se o usuário não estiver autenticado (user é null), redireciona para a página de login
    // 'replace' impede que o usuário volte para esta página pelo histórico do navegador
    if (!user) {
        return <Navigate to="/login" replace />;
    }

    // Se o usuário estiver autenticado, exibe suas informações
    return (
        <div style={{ maxWidth: '600px', margin: '50px auto', padding: '30px', border: '1px solid #eee', borderRadius: '10px', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
            <h2 style={{ textAlign: 'center', marginBottom: '30px', color: '#333' }}>Meu Perfil</h2>
            <div style={{ fontSize: '1.1em', lineHeight: '1.6' }}>
                <p><strong>Nome:</strong> {user.name}</p>
                <p><strong>Email:</strong> {user.email}</p>
                {user.created_at && ( // Verifica se created_at existe antes de formatar
                    <p><strong>Membro desde:</strong> {new Date(user.created_at).toLocaleDateString('pt-BR')}</p>
                )}
                {/* Adicione outras informações do usuário se disponíveis no seu schema 'User' do backend */}
                {/* Ex: <p><strong>Gêneros Favoritos:</strong> {user.favorite_genres?.map(g => g.name).join(', ')}</p> */}
            </div>
        </div>
    );
}

export default ProfilePage;