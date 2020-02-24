FROM jupyter/scipy-notebook

COPY conf/requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER
	
COPY conf/jupyter_notebook_config.py /etc/jupyter/
COPY conf/jupyter_notebook_config.py /home/jovyan/.jupyter