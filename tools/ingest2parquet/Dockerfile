FROM docker.io/rayproject/ray:2.9.3-py310

# install pytest
RUN pip install --no-cache-dir pytest

# Copy in the data processing framework source/project and install it
# This is expected to be placed in the docker context before this is run (see the make image).
COPY --chown=ray:users data-processing-lib/ data-processing-lib/
# install data processing
RUN cd data-processing-lib && pip install --no-cache-dir -e .

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r  requirements.txt

RUN rm requirements.txt
# copy source
COPY --chown=ray:users ./src .
# copy test
COPY --chown=ray:users test/ test/
COPY --chown=ray:users test-data/ test-data/
# Set environment
ENV PYTHONPATH /home/ray
