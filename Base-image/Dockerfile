ARG debian_buster_image_tag=8-jre-slim
FROM openjdk:${debian_buster_image_tag}


ARG shared_workspace=/opt/workspace

RUN mkdir -p ${shared_workspace} && \
    apt-get update -y && \
    rm -rf /var/lib/apt/lists/*

ENV SHARED_WORKSPACE=${shared_workspace}


VOLUME ${shared_workspace}
CMD ["bash"]
