FROM public.ecr.aws/lambda/python:3.8

RUN yum update -y
RUN yum install wget -y
# pyvista の実行に失敗する
RUN yum install mesa-libGL-devel -y
RUN yum clean all

# RUN yum update && yum install -y wget && yum clean all
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
RUN sh miniconda.sh -b -p /opt/miniconda

COPY environment.yml /tmp/environment.yml
RUN sed -i -r '/m2w64|vs2015|msys2|win|vc/d' /tmp/environment.yml
RUN /opt/miniconda/bin/conda env create --file /tmp/environment.yml --prefix /opt/conda-env

# aws lambda 用のモジュール
RUN /opt/conda-env/bin/pip install awslambdaric

# 既存のpython ファイルを消す
RUN rm /var/lang/bin/python3.8
# conda の環境を 既存のpython ファイルの場所に入れる
RUN ln -sf /opt/conda-env/bin/python /var/lang/bin/python3.8

# 本プロジェクトのソースファイルをコピー
COPY aws_lambda.py /opt/my-code/app.py
COPY ./src  /opt/my-code/src

# 環境変数をセットする
ENV PYTHONPATH "/var/lang/lib/python3.8/site-packages:/opt/my-code"

ENV PYVISTA_USERDATA_PATH "/tmp"

ENTRYPOINT ["/lambda-entrypoint.sh"]

CMD ["app.lambda_handler"]