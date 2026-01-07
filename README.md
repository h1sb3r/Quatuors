# 🎮 Quatuors

Une adaptation en français du célèbre jeu de logique **Connections**.
Trouvez les 4 groupes de 4 mots liés par un thème commun !

<img width="608" height="545" alt="image" src="https://github.com/user-attachments/assets/6e1f0d27-3da9-4846-a0fb-e79dcfe607bc" />


## 🔗 Jouer en ligne
👉 **[Accéder au jeu (Site Web)](https://h1sb3r.github.io/Quatuors/)**

---

## 🛠 Fonctionnement technique
Ce projet est un site statique léger + un petit serveur local pour éditer :
*   **index.html** : Le jeu (HTML/CSS/JS).
*   **studio.html** : L'éditeur pour créer/dupliquer des jeux.
*   **data.json** : Contient tous les jeux (4 catégories x 4 mots).
*   **server.py** : Serveur local + endpoints de sauvegarde/push.

## 🧰 Studio local (édition + push)
1. Lancez le serveur : `python server.py`
2. Ouvrez `http://localhost:8000/studio.html`
3. Ajoutez vos catégories et mots, puis cliquez sur **Sauvegarder**.
4. Cliquez sur **Push GitHub** pour publier.

## 📝 Structure des données
Chaque jeu contient exactement 4 catégories de 4 mots :
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
