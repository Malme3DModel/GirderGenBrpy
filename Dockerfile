FROM continuumio/miniconda3

# # ifcOpenshell のアーカイブをダウンロード
# RUN wget https://s3.amazonaws.com/ifcopenshell-builds/ifcopenshell-python-39-v0.7.0-e508fb4-linux64.zip
# # ifcOpenshell のアーカイブを解凍
# RUN apt-get update
# RUN apt-get install unzip
# RUN unzip ifcopenshell-python-39-v0.7.0-e508fb4-linux64.zip
# RUN rm ifcopenshell-python-39-v0.7.0-e508fb4-linux64.zip
# # ifcOpenshell をコピー
# RUN mv ifcopenshell /opt/conda/lib/python3.9/site-packages

RUN apt-get update
RUN apt-get install libgl1-mesa-dev

RUN conda install -c conda-forge ifcopenshell
RUN conda install -c conda-forge pyvista
RUN conda install -c conda-forge meshio






COPY app.py   ./
COPY ./src   ./src

CMD ["app.handler"]  