// frontend/src/pages/HomePage.js
import React, { useState, useEffect } from 'react';
import api from '../services/api'; // Importa a instância do axios configurada
import { Link } from 'react-router-dom'; // Para links de navegação

function HomePage() {
    const [searchTerm, setSearchTerm] = useState('');
    const [movies, setMovies] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [nowPlayingMovies, setNowPlayingMovies] = useState([]);

    // Função para buscar filmes em cartaz
    const fetchNowPlayingMovies = async () => {
        setLoading(true);
        try {
            // Endpoint do backend: GET /em_cartaz?regiao=BR
            const response = await api.get('/em_cartaz', { params: { regiao: 'BR' } });
            // Ajuste aqui se a estrutura da sua resposta for diferente (ex: response.data.results)
            setNowPlayingMovies(response.data.results || response.data);
        } catch (err) {
            console.error('Erro ao buscar filmes em cartaz:', err);
            setError('Erro ao carregar filmes em cartaz.');
        } finally {
            setLoading(false);
        }
    };

    // Efeito para carregar os filmes em cartaz ao montar o componente
    useEffect(() => {
        fetchNowPlayingMovies();
    }, []);

    // Função para lidar com a busca de filmes
    const handleSearch = async (e) => {
        e.preventDefault(); // Previne o comportamento padrão do formulário
        if (!searchTerm) {
            setMovies([]); // Limpa os resultados se a busca estiver vazia
            return;
        }
        setLoading(true);
        setError(null);
        try {
            // Endpoint do backend: GET /filmes/search?q={query}
            const response = await api.get(`/filmes/search?query=${searchTerm}`);
            setMovies(response.data); // Assumindo que retorna uma lista de filmes
        } catch (err) {
            console.error('Erro ao buscar filmes:', err);
            setError(err.response?.data?.detail || 'Erro ao buscar filmes.');
            setMovies([]); // Limpa resultados em caso de erro
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h1>CineBase</h1>

            <section style={{ marginBottom: '40px' }}>
                <h2>Filmes em Cartaz</h2>
                {loading && <p>Carregando filmes em cartaz...</p>}
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', justifyContent: 'center' }}>
                    {nowPlayingMovies.length > 0 ? (
                        nowPlayingMovies.map((movie) => (
                            <div key={movie.id} style={{ border: '1px solid #ccc', borderRadius: '8px', overflow: 'hidden', width: '200px', boxShadow: '2px 2px 8px rgba(0,0,0,0.1)' }}>
                                <Link to={`/filmes/${movie.id}`}>
                                    {movie.poster_path && ( // Use poster_path do TMDB
                                        <img
                                            src={`https://image.tmdb.org/t/p/w200${movie.poster_path}`}
                                            alt={movie.title}
                                            style={{ width: '100%', height: 'auto', display: 'block' }}
                                        />
                                    )}
                                </Link>
                                <div style={{ padding: '10px' }}>
                                    <h3>{movie.title}</h3>
                                    <p style={{ fontSize: '0.9em', color: '#555' }}>Lançamento: {movie.release_date}</p>
                                    <Link to={`/filmes/${movie.id}`} style={{ textDecoration: 'none', color: 'blue' }}>Detalhes</Link>
                                </div>
                            </div>
                        ))
                    ) : (
                        !loading && <p>Nenhum filme em cartaz encontrado.</p>
                    )}
                </div>
            </section>

            <hr style={{ margin: '40px 0', borderColor: '#eee' }} />

            <section>
                <h2>Buscar Filmes</h2>
                <form onSubmit={handleSearch} style={{ marginBottom: '20px' }}>
                    <input
                        type="text"
                        placeholder="Buscar filme por nome..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        style={{ padding: '8px', width: '300px', marginRight: '10px', borderRadius: '4px', border: '1px solid #ccc' }}
                    />
                    <button type="submit" style={{ padding: '8px 15px', borderRadius: '4px', border: 'none', background: '#007bff', color: 'white', cursor: 'pointer' }}>Buscar</button>
                </form>

                {loading && <p>Carregando resultados...</p>}
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '20px', justifyContent: 'center' }}>
                    {movies.length > 0 ? (
                        movies.map((movie) => (
                            <div key={movie.id} style={{ border: '1px solid #ccc', borderRadius: '8px', overflow: 'hidden', width: '200px', boxShadow: '2px 2px 8px rgba(0,0,0,0.1)' }}>
                                <Link to={`/filmes/${movie.id}`}>
                                    {movie.poster_url && ( // Use poster_url do seu DB
                                        <img
                                            src={`https://image.tmdb.org/t/p/w200${movie.poster_url}`}
                                            alt={movie.title}
                                            style={{ width: '100%', height: 'auto', display: 'block' }}
                                        />
                                    )}
                                </Link>
                                <div style={{ padding: '10px' }}>
                                    <h3>{movie.title}</h3>
                                    <p style={{ fontSize: '0.9em', color: '#555' }}>Lançamento: {movie.release_date}</p>
                                    <Link to={`/filmes/${movie.id}`} style={{ textDecoration: 'none', color: 'blue' }}>Detalhes</Link>
                                </div>
                            </div>
                        ))
                    ) : (
                        !loading && searchTerm && <p>Nenhum filme encontrado para "{searchTerm}".</p>
                    )}
                </div>
            </section>
        </div>
    );
}

export default HomePage;