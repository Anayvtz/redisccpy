
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

.PHONY: run_srvr

run_srvr: $(VENV)/bin/activate
	$(PYTHON) main_srvr.py resp.py srvr.py

run_clnt: $(VENV)/bin/activate
	$(PYTHON) main_clnt.py

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	pip install -r requirements.txt

.PHONY: clean

clean:  
	rm -f  /tmp/core* core 
	rm -rf __pycache__
	rm -rf $(VENV)
