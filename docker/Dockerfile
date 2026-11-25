FROM ubuntu:latest AS pyra2yr

RUN dpkg --add-architecture i386

RUN \ 
	apt-get update -y && apt-get install -y \
	bash \
	python3 \
	python3-pip \
	wine32

# In new distros, wine has removed the /usr/bin/wineserver launcher.
# Restore it here, so it can be found in PATH.
# wine 10.0~repack-12
# - https://changelogs.ubuntu.com/changelogs/pool/universe/w/wine/wine_10.0~repack-12ubuntu1/changelog
# - https://tracker.debian.org/news/1693766/accepted-wine-100repack-12-source-into-unstable/
RUN if ! command -v wineserver >/dev/null; then \
        ln -s /usr/lib/i386-linux-gnu/wine/wineserver /usr/local/bin/wineserver; \
    fi && wineserver --version

# Create user and necessary folders
RUN useradd -m user && mkdir -p /home/user/project /home/user/.wine && chmod -R 0777 /home/user

RUN apt-get clean -y && \
	rm -rf /var/lib/apt/lists/*