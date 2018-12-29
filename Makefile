all: resources

resources:
	pyrcc5 -o systray_rc.py systray.qrc

clean:
	rm -rf *.pyc */*.pyc */*/*.pyc
