FROM python:3.7-slim
# for PyInstaller: binutils libc-bin
# for flyer-composer: python3-qt5 qttranslations5-l10n
# for tar -xz: xz-utils
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
		python3-pyqt5 qttranslations5-l10n \
		binutils libc-bin xz-utils \
	&& rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir PyMuPdf pyinstaller
ENV PYTHONPATH=/usr/lib/python3/dist-packages

# Replace 1000 with your user / group id
RUN addgroup --gid 1000 developer && \
	adduser  --uid 1000 --ingroup developer --disabled-password \
	         developer </dev/null || true

USER developer
WORKDIR /home/developer
CMD /bin/bash
