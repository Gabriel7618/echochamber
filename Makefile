PYTHON = python3
SRC = classifier.py extractcontent.py getarticles.py main.py
EXECUTABLE = echochamber

all: $(EXECUTABLE)

$(EXECUTABLE): $(SRC)
	echo "#!/usr/bin/env $(PYTHON)" > $(EXECUTABLE)
	cat main.py >> $(EXECUTABLE)
	chmod +x $(EXECUTABLE)

clean:
	rm -f $(EXECUTABLE)