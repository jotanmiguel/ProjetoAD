PRAGMA foreign_keys = ON;

CREATE TABLE utilizadores (id INTEGER PRIMARY KEY, nome TEXT, senhaTEXT);

CREATE TABLE musicas(
    id INTEGER PRIMARY KEY,
    id_spotifyTEXT,
    nomeTEXT,
    id_artistaINTEGER,
    FOREIGN KEY(id_artista) REFERENCES artistas(id) ON DELETE CASCADE
);

CREATE TABLE artistas(idINTEGER PRIMARY KEY, id_spotifyTEXT, nomeTEXT);

CREATE TABLE avaliacoes (idINTEGER PRIMARY KEY, siglaTEXT, designacaoTEXT);

CREATE TABLE playlists(
    id_userINTEGER,
    id_musicaINTEGER,
    id_avaliacaoINTEGER,
    PRIMARY KEY (id_user, id_musica),
    FOREIGN KEY(id_user) REFERENCES utilizadores(id) ON DELETE CASCADE,
    FOREIGN KEY(id_musica) REFERENCES musicas(id) ON DELETE CASCADE,
    FOREIGN KEY(id_avaliacao) REFERENCES avaliacoes(id) ON DELETE CASCADE
);

INSERT INTO
    avaliacoes(id, sigla, designacao)
VALUES
    (1, "M", "Medíocre"),
    (2, "m", "Mau"),
    (3, "S", "Suficiente"),
    (4, "B", "Boa"),
    (5, "MB", "Muito Boa");