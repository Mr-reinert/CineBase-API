// frontend/src/pages/MovieDetailPage.js
import React, { useState, useEffect, useCallback } from 'react'; // Adicione useCallback aqui
import { useParams } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../contexts/AuthContext';

function MovieDetailPage() {
    const { id } = useParams();
    const [movie, setMovie] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [newReviewRating, setNewReviewRating] = useState(5);
    const [newReviewComment, setNewReviewComment] = useState('');
    const { user } = useAuth();

    // Envolva fetchMovieDetailsAndReviews com useCallback
    const fetchMovieDetailsAndReviews = useCallback(async () => {
        setLoading(true);
        try {
            const movieResponse = await api.get(`/filmes/${id}`);
            setMovie(movieResponse.data);

            const reviewsResponse = await api.get(`/filmes/${id}/avaliacoes`);
            setReviews(reviewsResponse.data);

        } catch (err) {
            console.error('Erro ao buscar detalhes do filme ou avaliações:', err);
            setError(err.response?.data?.detail || 'Erro ao carregar detalhes do filme.');
        } finally {
            setLoading(false);
        }
    }, [id]); // Adicione 'id' como dependência do useCallback, pois a função o utiliza

    // Agora, adicione fetchMovieDetailsAndReviews na matriz de dependências do useEffect
    useEffect(() => {
        fetchMovieDetailsAndReviews();
    }, [fetchMovieDetailsAndReviews]); // A dependência agora é a função memorizada

    const handleReviewSubmit = async (e) => {
        e.preventDefault();
        if (!user) {
            alert('Você precisa estar logado para fazer uma avaliação.');
            return;
        }
        try {
            const response = await api.post(`/filmes/${id}/avaliacoes`, {
                rating: newReviewRating,
                comment: newReviewComment,
            });
            setReviews([...reviews, response.data]);
            setNewReviewRating(5);
            setNewReviewComment('');
            alert('Avaliação adicionada com sucesso!');
        } catch (err) {
            console.error('Erro ao enviar avaliação:', err.response?.data?.detail || err.message);
            alert('Erro ao enviar avaliação: ' + (err.response?.data?.detail || 'Erro desconhecido.'));
        }
    };

    if (loading) return <p>Carregando detalhes do filme...</p>;
    if (error) return <p style={{ color: 'red' }}>{error}</p>;
    if (!movie) return <p>Filme não encontrado.</p>;

    return (
        <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
            <h2 style={{ marginBottom: '20px' }}>{movie.title}</h2>

            <div style={{ display: 'flex', gap: '30px', alignItems: 'flex-start', marginBottom: '30px' }}>
                {movie.poster_url && (
                    <img
                        src={`https://image.tmdb.org/t/p/w300${movie.poster_url}`}
                        alt={movie.title}
                        style={{ borderRadius: '8px', boxShadow: '0 4px 10px rgba(0,0,0,0.1)' }}
                    />
                )}
                <div>
                    <p><strong>Sinopse:</strong> {movie.overview}</p>
                    <p><strong>Data de Lançamento:</strong> {movie.release_date}</p>
                    {movie.budget !== null && movie.budget !== undefined && movie.budget !== 0 && (
                        <p><strong>Orçamento:</strong> ${movie.budget.toLocaleString('pt-BR')}</p>
                    )}
                </div>
            </div>

            <section style={{ marginBottom: '40px' }}>
                <h3>Avaliações</h3>
                {reviews.length > 0 ? (
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                        {reviews.map((review) => (
                            <li key={review.id} style={{ borderBottom: '1px solid #eee', paddingBottom: '15px', marginBottom: '15px' }}>
                                <strong>Avaliação:</strong> {review.rating}/10
                                {review.comment && <p style={{ margin: '5px 0 0 0' }}>"{review.comment}"</p>}
                                <small style={{ color: '#777' }}>
                                    Por Usuário {review.user_id} em {new Date(review.created_at).toLocaleDateString('pt-BR')}
                                </small>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>Nenhuma avaliação ainda. Seja o primeiro a avaliar!</p>
                )}
            </section>

            {user ? (
                <section>
                    <h3>Deixe sua avaliação</h3>
                    <form onSubmit={handleReviewSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                        <div>
                            <label style={{ display: 'block', marginBottom: '5px' }}>Nota (1-10):</label>
                            <input
                                type="number"
                                min="1"
                                max="10"
                                value={newReviewRating}
                                onChange={(e) => setNewReviewRating(parseInt(e.target.value))}
                                required
                                style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc', width: '100px' }}
                            />
                        </div>
                        <div>
                            <label style={{ display: 'block', marginBottom: '5px' }}>Comentário:</label>
                            <textarea
                                value={newReviewComment}
                                onChange={(e) => setNewReviewComment(e.target.value)}
                                rows="4"
                                cols="50"
                                style={{ padding: '8px', borderRadius: '4px', border: '1px solid #ccc', width: '100%' }}
                            ></textarea>
                        </div>
                        <button type="submit" style={{ padding: '10px 20px', borderRadius: '4px', border: 'none', background: '#28a745', color: 'white', cursor: 'pointer', alignSelf: 'flex-start' }}>
                            Enviar Avaliação
                        </button>
                    </form>
                </section>
            ) : (
                <p style={{ textAlign: 'center', marginTop: '30px', padding: '15px', background: '#f8d7da', color: '#721c24', border: '1px solid #f5c6cb', borderRadius: '5px' }}>
                    Faça login para deixar uma avaliação.
                </p>
            )}
        </div>
    );
}

export default MovieDetailPage;