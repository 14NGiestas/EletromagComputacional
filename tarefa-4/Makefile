define check_tkinter =

if python -c 'import tkinter';
then
	echo '[Sucesso] Tk/Tcl está instalado!'
else
	echo '[Falhou] Por favor, instale Tk/Tcl'
fi

endef

setup:
	@echo "Instalando dependencias"
	@pip install -r requirements.txt --user
	@echo "Verificando Tk/Tcl está instalado"
	@$(value check_tkinter)

run:
	@python src/main.py

.ONESHELL:
