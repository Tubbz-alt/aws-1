FROM continuumio/miniconda3

# Get the environment file
ADD environment.yaml /tmp/environment.yaml
RUN conda config --add channels conda-forge \
    && conda env create -n enram-store -f /tmp/environment.yaml \
    && rm -rf /opt/conda/pkgs/*

ENV PATH /opt/conda/envs/enram-store/bin:$PATH

# Copy the entire project and build
COPY ./datamover/* /app/datamover/
COPY ./task.py /app/

# Start the defined task
CMD [ "python", "/app/task.py" ]

