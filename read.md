como teste pra pegar os dados para o "em_cartaz" usei esse link
https://api.themoviedb.org/3/movie/now_playing?api_key=a5e352e95167d38103968d7ca7609755

usei isso pra evitar de criar o pycache
echo 'export PYTHONDONTWRITEBYTECODE=1' >> ~/.bashrc


se quiser subir a api no servidor use:
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

    pra usar no terminal pra subir a api em segundo plano:
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload &   

