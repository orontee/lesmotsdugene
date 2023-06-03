# Site lesmotsdugene

Version statique du site de l'association «Les mots du Gène».

## Pré-requis

- Python 3.9

## Génération

Dans un terminal, exécuter les commandes suivantes (en adaptant le
port selon l'environnement) :

```
$ python3 -m venv env
$ source env/bin/activate
(env)$ python -m pip install -r requirements.txt
(env)$ make devserver PORT=8000
```

Ensuite consulter l'adresse [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Publication

Après avoir configuré [l'interface de ligne de
commande](https://aws.amazon.com/fr/cli/) :

```
$ make rsync_upload
```

Le site est consultable à l'adresse https://lesmotsdugene.alwaysdata.net/.

## Notes

* Le thème est dérivé du thème par défaut de
  [Pelican](https://github.com/getpelican/pelican).

* Les vidéos sont stockées sur le *bucket* AWS S3 `s3://lesmotsdugene-test`
  et servies via https://d1njpgd0ygatdn.cloudfront.net
