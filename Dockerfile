FROM zilzalll/zthon:slim-buster

RUN git clone https://github.com/Zilzalll/ZThon.git /root/zira

WORKDIR /root/zira

RUN curl -sL https://deb.nodesource.com/setup_16.x | bash -
RUN apt-get install -y nodejs
RUN npm i -g npm
RUN pip3 install --no-cache-dir -r requirements.txt

ENV PATH="/home/zira/bin:$PATH"

CMD ["python3","-m","zira"]
