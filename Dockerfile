FROM duckietown/dt-duckiebot-interface:daffy-arm32v7

WORKDIR /colour_detector_dir

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY colour_detector.py .
ENV N_SPLITS 20
CMD python3 ./colour_detector.py
