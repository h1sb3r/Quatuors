# Quatuors

Une adaptation en francais du jeu de logique Connections.

## Structure

- `index.html` : jeu public statique
- `data.json` : donnees des jeux
- `Audio/` : sons utilises par le jeu
- `local/studio.html` : studio d'edition, local uniquement
- `local/server_impl.py` : serveur local et endpoints API
- `server.py` : point d'entree compatible pour lancer le serveur local

## Jeu public

Le jeu public repose uniquement sur :

- `index.html`
- `data.json`
- `favicon.ico`
- `Audio/`

Cette partie est compatible avec GitHub Pages et prete pour un deploiement Vercel.

## Studio local

Le studio n'est pas concu pour etre publie.

1. Lancez `launch-studio.cmd` ou `python server.py`
2. Ouvrez `http://localhost:8081/local/studio.html` si vous utilisez `launch-studio.cmd`
3. Sinon ouvrez `http://localhost:8000/local/studio.html`
4. Ajoutez ou modifiez les jeux
5. Cliquez sur `Sauvegarder`, puis `Push GitHub` si besoin

## Lancement rapide

- `launch_quatuors.bat` : ouvre le jeu local
- `launch-studio.cmd` : ouvre le studio local

## Structure des donnees

Chaque jeu contient exactement 4 categories de 4 mots :

```json
{
  "games": [
    {
      "id": "2026-01-07",
      "title": "Jeu du 7 jan 2026",
      "groups": [
        { "category": "EXEMPLE", "color": "#f9df6d", "items": ["A", "B", "C", "D"] }
      ]
    }
  ]
}
```
