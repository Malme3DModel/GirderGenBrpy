FROM public.ecr.aws/lambda/python:3.9

RUN yum update -y
RUN yum install wget -y

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh -O ~/Miniconda.sh
RUN /bin/bash ~/Miniconda.sh -b -p ~/miniconda3
RUN rm ~/Miniconda.sh
RUN echo ". ~/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc
RUN echo "conda activate base" >> ~/.bashrc

ENV PATH /root/miniconda3/bin:$PATH

RUN yum install mesa-libGL-devel -y
RUN conda install -c conda-forge ifcopenshell
RUN conda install -c conda-forge pyvista
RUN conda install -c conda-forge meshio
# Install the function's dependencies
RUN pip install awslambdaric

# RUN chmod 644 $(find /root/miniconda3/bin -type f)
# RUN chmod 755 $(find /root/miniconda3/bin -type d)

# 自分のモジュールをコピー
COPY app.py ./
COPY ./src  ./src
# RUN mkdir   ./tmp

# テストコードもコピーしておいて
COPY ./tests ./tests

# entry point を miniconda に変更 /var/runtime/bootstrap が既存のpythonを指定しているので入れ替え
COPY bootstrap /var/runtime/bootstrap
COPY bootstrap.py /var/runtime/bootstrap.py
# RUN chmod 755 /var/runtime/bootstrap
# ENTRYPOINT [ "/lambda-entrypoint.sh" ]
# ENTRYPOINT [ "/root/miniconda3/bin/python", "-m", "awslambdaric" ]

CMD ["app.handler"]