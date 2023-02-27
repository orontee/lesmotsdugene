# Site lesmotsdugene

Version statique du site de l'association «Les mots du Gène».

## Pré-requis

- Python 3.9

## Génération

Dans un terminal, exécuter les commandes suivantes :

```
$ python3 -m venv env
$ source env/bin/activate
(env)$ python -m pip install -r requirements.txt
(env)$ pelican content
(env)$ pelican --listen
```

Ensuite consulter l'adresse [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Notes

* Le thème est dérivé du thème par défaut de
  [Pelican](https://github.com/getpelican/pelican).
