FROM centos:7
LABEL authors="Antoni Segura Puimedon<toni@kuryr.org>, Michał Dulko<mdulko@redhat.com>"

ARG UPPER_CONSTRAINTS_FILE="https://git.openstack.org/cgit/openstack/requirements/plain/upper-constraints.txt"

RUN yum install -y epel-release \
    && yum install -y --setopt=tsflags=nodocs python-pip \
    && yum install --setopt=tsflags=nodocs --assumeyes inet-tools gcc python-devel wget git \
    && pip install -U setuptools

COPY . /opt/kuryr-kubernetes

RUN cd /opt/kuryr-kubernetes \
    && pip install -c $UPPER_CONSTRAINTS_FILE --no-cache-dir . \
    && rm -fr .git \
    && yum -y history undo last \
    && groupadd -r kuryr -g 711 \
    && useradd -u 711 -g kuryr \
         -d /opt/kuryr-kubernetes \
         -s /sbin/nologin \
         -c "Kuryr controller user" \
         kuryr \
    && chown kuryr:kuryr /opt/kuryr-kubernetes

USER kuryr
CMD ["--config-dir", "/etc/kuryr"]
ENTRYPOINT [ "/usr/bin/kuryr-k8s-controller" ]
