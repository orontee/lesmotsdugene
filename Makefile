PY?=
PELICAN?=pelican
PELICANOPTS=-e GIT_VERSION_STRING='"$(shell git describe --tags --match "v[0-9]*")"'

BASEDIR=$(CURDIR)
INPUTDIR=$(BASEDIR)/content
OUTPUTDIR=$(BASEDIR)/output
CONFFILE=$(BASEDIR)/pelicanconf.py
PUBLISHCONF=$(BASEDIR)/publishconf.py

SSH_PORT=22
SSH_USER=lesmotsdugene
SSH_HOST=ssh-lesmotsdugene.alwaysdata.net
SSH_TARGET_DIR=static-site

DEBUG ?= 0
ifeq ($(DEBUG), 1)
	PELICANOPTS += -D
endif

RELATIVE ?= 0
ifeq ($(RELATIVE), 1)
	PELICANOPTS += --relative-urls
endif

SERVER ?= "0.0.0.0"

PORT ?= 0
ifneq ($(PORT), 0)
	PELICANOPTS += -p $(PORT)
endif


help:
	@echo 'Makefile for a pelican Web site                                           '
	@echo '                                                                          '
	@echo 'Usage:                                                                    '
	@echo '   make html                           (re)generate the web site          '
	@echo '   make clean                          remove the generated files         '
	@echo '   make publish                        generate using production settings '
	@echo '   make serve [PORT=8000]              serve site at http://localhost:8000'
	@echo '   make serve-global [SERVER=0.0.0.0]  serve (as root) to $(SERVER):80    '
	@echo '   make devserver [PORT=8000]          serve and regenerate together      '
	@echo '   make devserver-global               regenerate and serve on 0.0.0.0    '
	@echo '   make ssh_upload                     upload the web site via SSH        '
	@echo '   make sftp_upload                    upload the web site via SFTP       '
	@echo '   make rsync_upload                   upload the web site via rsync+ssh  '
	@echo '                                                                          '
	@echo 'Set the DEBUG variable to 1 to enable debugging, e.g. make DEBUG=1 html   '
	@echo 'Set the RELATIVE variable to 1 to enable relative urls                    '
	@echo '                                                                          '

html:
	"$(PELICAN)" "$(INPUTDIR)" \
					 --output "$(OUTPUTDIR)" \
					 --settings "$(CONFFILE)" \
					 $(PELICANOPTS)
	python3 -m pagefind --site "$(OUTPUTDIR)"

clean:
	[ ! -d "$(OUTPUTDIR)" ] || rm -rf "$(OUTPUTDIR)"

serve: html
	"$(PELICAN)" "$(INPUTDIR)" \
					 --listen \
					 --output "$(OUTPUTDIR)" \
					 --settings "$(CONFFILE)" \
					 $(PELICANOPTS)

serve-global: html
	"$(PELICAN)" "$(INPUTDIR)" \
					 --listen \
					 --output "$(OUTPUTDIR)" \
					 --settings "$(CONFFILE)" \
					 --bind $(SERVER) \
					 $(PELICANOPTS)

devserver: html
	"$(PELICAN)" "$(INPUTDIR)" \
					 --listen \
					 --autoreload \
					 --output "$(OUTPUTDIR)" \
					 --settings "$(CONFFILE)" \
					 $(PELICANOPTS)

devserver-global: html
	$(PELICAN) "$(INPUTDIR)" \
				  --listen \
				  --autoreload \
				  --output $(OUTPUTDIR) \
				  --settings $(CONFFILE) \
				  --bind  0.0.0.0 \
				  $(PELICANOPTS)

publish: clean
	"$(PELICAN)" "$(INPUTDIR)" \
					 --output "$(OUTPUTDIR)" \
					 --settings "$(PUBLISHCONF)" \
					 $(PELICANOPTS)
	python3 -m pagefind --site "$(OUTPUTDIR)"

ssh_upload: publish
	scp -P $(SSH_PORT) -r "$(OUTPUTDIR)"/* \
		 "$(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)"

sftp_upload: publish
	printf 'put -r $(OUTPUTDIR)/*' | \
		sftp $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)

rsync_upload: publish
	rsync -e "ssh -p $(SSH_PORT)" \
			-P -rvzc --include tags --cvs-exclude --delete \
			"$(OUTPUTDIR)"/ "$(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)"

.PHONY: html help clean serve serve-global devserver publish
.PHONY: ssh_upload sftp_upload rsync_upload
