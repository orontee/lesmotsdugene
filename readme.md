# Site lesmotsdugene

Version statique du site de l'association «Les mots du Gène».

## Pré-requis

- Python >3.9

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

Il est possible de publier via SSH, après avoir configuré l'accès SSH au 
serveur hôte (cf. [Makefile](./Makefile) pour la configuration) :
```
(env)$ make rsync_upload
```

Mais actuellement le site est publié avec [Github
Pages](https://docs.github.com/fr/pages) via la branche `gh_pages`
(poser un tag Git avant d'exécuter ces commandes pour que le site
affiche une version correspondante) :

```
(env)$ python -m pip install ghp-import
(env)$ make publish
(env)$ 
(env)$ ghp-import output \
                  --cname=lesmotsdugene.fr \
				  --message="Publication de la version $(git describe --tags --match "v[0-9]*")" \
				  --branch=gh-pages \
				  --push
```

Le site est consultable à l'adresse https://lesmotsdugene.fr.

### Conformité aux standards

Pour évaluer la conformité aux standards du Web, utiliser les outils
du [W3C](https://www.w3.org/) :

* [Nu Html Checker](https://validator.w3.org/nu/?doc=https%3A%2F%2Flesmotsdugene.fr%2F)

* [Validateur CSS](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Flesmotsdugene.fr&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=fr)


## Notes

* Le thème est dérivé du thème par défaut de
  [Pelican](https://github.com/getpelican/pelican).

* Les vidéos sont stockées sur le *bucket* AWS S3 `s3://lesmotsdugene-test`
  et servies via https://d1njpgd0ygatdn.cloudfront.net
