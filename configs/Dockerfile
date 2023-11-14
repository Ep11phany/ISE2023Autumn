FROM python:3.10
WORKDIR .

COPY requirements.txt .

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install torchvision torch -i https://pypi.tuna.tsinghua.edu.cn/simple

RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

RUN python ./import_images.py

CMD ["python", "./server.py"]