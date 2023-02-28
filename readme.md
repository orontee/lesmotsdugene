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
(env)$ invoke reserve
```

Ensuite consulter l'adresse [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Publication

Après avoir configuré [l'interface de ligne de
commande](https://aws.amazon.com/fr/cli/) :

```
$ make s3_upload
```

Le site est consultable à l'adresse
http://lesmotsdugene-test.s3-website.eu-west-3.amazonaws.com/.

## Notes

* Le thème est dérivé du thème par défaut de
  [Pelican](https://github.com/getpelican/pelican).
