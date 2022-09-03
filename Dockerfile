FROM continuumio/miniconda3

RUN conda create -n ifcos python==3.8

SHELL ["conda", "run", "-n", "ifcos", "/bin/bash", "-c"]
RUN conda install -c conda-forge -c oce -c dlr-sc -c ifcopenshell ifcopenshell
RUN conda install -c conda-forge pyvista

ENV LANG=en_US.UTF-8
ENV TZ=:/etc/localtime
ENV PATH=/var/lang/bin:/usr/local/bin:/usr/bin/:/bin:/opt/bin
ENV LD_LIBRARY_PATH=/var/lang/lib:/lib64:/usr/lib64:/var/runtime:/var/runtime/lib:/var/task:/var/task/lib:/opt/lib
ENV LAMBDA_TASK_ROOT=/var/task
ENV LAMBDA_RUNTIME_DIR=/var/runtime

WORKDIR /var/task

ENTRYPOINT ["/lambda-entrypoint.sh"]


COPY app.py   /var/task
COPY ./src   /var/task/src

CMD ["app.handler"]  