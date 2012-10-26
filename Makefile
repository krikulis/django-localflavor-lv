test:
	pep8 --ignore=E128,E501 django_localflavor_lv
	coverage run --branch --source=django_localflavor_lv `which django-admin.py` test --settings=django_localflavor_lv.tests.settings django_localflavor_lv
	coverage report --omit=django_localflavor_lv/test*

