FROM public.ecr.aws/lambda/python:3.8

RUN yum update -y
RUN yum install wget -y 

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py39_4.9.2-Linux-x86_64.sh -O ~/Miniconda.sh 
RUN /bin/bash ~/Miniconda.sh -b -p ~/miniconda3
RUN rm ~/Miniconda.sh 
# echo ". ~/miniconda3/etc/profile.d/conda.sh" >> ~/.bashrc
# echo "conda activate base" >> ~/.bashrc

ENV PATH ~/miniconda3/bin:$PATH

RUN yum install mesa-libGL-devel -y 
RUN conda install -c conda-forge ifcopenshell
RUN conda install -c conda-forge pyvista
RUN conda install -c conda-forge meshio

# 自分のモジュールをコピー
COPY app.py   ./
COPY ./src   ./src

CMD ["app.handler"]  