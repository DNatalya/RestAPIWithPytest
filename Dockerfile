FROM python
WORKDIR /test_project/
COPY requirements.txt .
RUN pip install -r requirements.txt && mkdir /logs
CMD python3 -m pytest -s --alluredir=test_results/ /test_project/tests